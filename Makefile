# ---------------------------------------------------------------------------- #
#               ------- VARIABLES ------
# ---------------------------------------------------------------------------- #

# User defined
PYTHON_TARGET_VERSION:=3.11.13

UV_SOURCE_VERSION:=0.8.18
UV_TARGET_VERSION:=0.8.18

CUSTOMER_NAME:=custom
APP_NAME:=app-name
APP_NAME_SNAKE:=app_name

# Generated
IMAGE_TAG:=$(shell cz version --project)

PYTHON_VERSION:=$(shell uv run python --version | sed 's/Python //')
PYTHON_NO_PATCH_VERSION:=$(shell echo ${PYTHON_VERSION} | cut -d. -f1-2)
PYTHON_NO_PATCH_TARGET_VERSION:=$(shell echo ${PYTHON_TARGET_VERSION} | cut -d. -f1-2)
PYTHON_NO_PATCH_NO_DOT_VERSION:=$(shell echo ${PYTHON_NO_PATCH_VERSION} | tr -d .)
PYTHON_NO_PATCH_NO_DOT_TARGET_VERSION:=$(shell echo ${PYTHON_NO_PATCH_TARGET_VERSION} | tr -d .)

UV_VERSION:=$(shell uv self version | sed 's/uv //')

# ---------------------------------------------------------------------------- #
#               ------- Initialization ------
# ---------------------------------------------------------------------------- #
pre-requisites:
	curl -fLSs https://astral.sh/uv/install.sh | sh
	curl -fLSs https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
	brew install gitleaks hadolint ls-lint tokei dmno-dev/tap/varlock

init:
	uv sync --frozen --no-default-groups
	source .venv/bin/activate

init-dev:
	uv sync --frozen
	uv run prek install --install-hooks
	source .venv/bin/activate

init-test:
	uv sync --frozen --group test --no-default-groups
	source .venv/bin/activate

init-from-scratch:
	uv init --build-backend uv --managed-python --name ${APP_NAME} --python ${PYTHON_VERSION} --vcs git
	uv sync
	source .venv/bin/activate

init-windows:
	uv venv --python ${PYTHON_VERSION}
	uv pip install --editable .

# ---------------------------------------------------------------------------- #
#               ------- Pyenv ------
# ---------------------------------------------------------------------------- #
pyenv-init:
	pyenv install ${PYTHON_VERSION}

pyenv-activate:
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/${PYTHON_VERSION}_${CUSTOMER_NAME}_${APP_NAME}
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/${PYTHON_VERSION}/envs/${PYTHON_VERSION}_${CUSTOMER_NAME}_${APP_NAME}
	pyenv local ${PYTHON_VERSION}_${CUSTOMER_NAME}_${APP_NAME}

# ---------------------------------------------------------------------------- #
#               ------- Python version ------
# ---------------------------------------------------------------------------- #
bump-dockerfile:
	sed -i "s/${PYTHON_VERSION}/${PYTHON_TARGET_VERSION}/g" docker/Dockerfile
	sed -i "s/${PYTHON_VERSION}/${PYTHON_TARGET_VERSION}/g" docker/alpine.Dockerfile
	sed -i "s/${PYTHON_VERSION}/${PYTHON_TARGET_VERSION}/g" docker/wheel.Dockerfile
	git add docker/{Dockerfile,alpine.Dockerfile,wheel.Dockerfile}

bump-pre-commit:
	sed -i "s/${PYTHON_NO_PATCH_VERSION}/${PYTHON_NO_PATCH_TARGET_VERSION}/g" .pre-commit-config.yaml
	git add .pre-commit-config.yaml

bump-pyproject:
	sed -i "s/${PYTHON_NO_PATCH_VERSION}\"/${PYTHON_NO_PATCH_TARGET_VERSION}\"/g" pyproject.toml
	sed -i "s/${PYTHON_NO_PATCH_NO_DOT_VERSION}/${PYTHON_NO_PATCH_NO_DOT_TARGET_VERSION}/g" pyproject.toml
	git add pyproject.toml

bump-python:
	rm -f .python-version || true
	rm -rf .venv
	uv python install ${PYTHON_TARGET_VERSION}
	uv sync --frozen

python-bump-patch: bump-dockerfile bump-python

python-bump-minor: bump-dockerfile bump-pre-commit bump-pyproject bump-python

# ---------------------------------------------------------------------------- #
#               ------- Uv ------
# ---------------------------------------------------------------------------- #
uv-check-update:
	uv self update --dry-run

uv-update:
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" docker/Dockerfile
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" docker/alpine.Dockerfile
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" docker/wheel.Dockerfile
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" .pre-commit-config.yaml
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" Makefile
	sed -i "s/${UV_SOURCE_VERSION}/${UV_TARGET_VERSION}/g" pyproject.toml
	git add docker/{Dockerfile,alpine.Dockerfile,wheel.Dockerfile} .pre-commit-config.yaml Makefile pyproject.toml
	uv self update

# ---------------------------------------------------------------------------- #
#               ------- Requirements ------
# ---------------------------------------------------------------------------- #
requirement:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt

requirement-dev:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt --group dev --group lint

requirement-test:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt --group test

requirement-all:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt --group dev --group lint
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt --group test

# ---------------------------------------------------------------------------- #
#               ------- Run ------
# ---------------------------------------------------------------------------- #
run:
	${APP_NAME_SNAKE}

run-module:
	python -m ${APP_NAME_SNAKE}.main

run-program:
	python src/${APP_NAME_SNAKE}/main.py

run-uv:
	uv run ${APP_NAME_SNAKE}

# ---------------------------------------------------------------------------- #
#               ------- Debug ------
# ---------------------------------------------------------------------------- #
debug-module:
	python -m pdb -m ${APP_NAME_SNAKE}.main

debug-program:
	python -m pdb src/${APP_NAME_SNAKE}/main.py

debug-venv-program:
	python -m pdb .venv/lib/python3.11/site-packages/${APP_NAME_SNAKE}/main.py

# ---------------------------------------------------------------------------- #
#               ------- Test ------
# ---------------------------------------------------------------------------- #
test:
	python -m pytest --color=yes --durations=5 --verbose --config-file=test/pytest.ini test/

coverage:
	coverage run --rcfile=pyproject.toml -m pytest --color=yes --verbose --config-file=test/pytest.ini
	coverage report --show-missing

# ---------------------------------------------------------------------------- #
#               ------- Telemetry ------
# ---------------------------------------------------------------------------- #
init-telemetry:
	uv run opentelemetry-bootstrap -a requirements | uv pip install --requirement -

run-telemetry: init-telemetry
	opentelemetry-instrument \
	--service_name ${APP_NAME} \
	--logs_exporter console \
	--traces_exporter console \
    --metrics_exporter console \
	python src/${APP_NAME_SNAKE}/main.py

# ---------------------------------------------------------------------------- #
#               ------- Pre-commit Hooks ------
# ---------------------------------------------------------------------------- #
hook-install:
	prek install --install-hooks

hook-run:
	prek run --all-files

hook-update:
	prek auto-update

# ---------------------------------------------------------------------------- #
#               ------- Docker ------
# ---------------------------------------------------------------------------- #
get-tag:
	echo "export IMAGE_TAG=${IMAGE_TAG}"

pull-image:
	docker pull ${APP_NAME}:${IMAGE_TAG}

push-image:
	docker push ${APP_NAME}:${IMAGE_TAG}

run-healthcheck:
	docker exec ${APP_NAME} python healthcheck.py

# ---------------------------------------------------------------------------- #
#               ------- Docker Build ------
# ---------------------------------------------------------------------------- #
build-builder-image: clean
	export DOCKER_CONTENT_TRUST=1
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg UV_VERSION=${UV_VERSION} --file docker/Dockerfile --tag ${APP_NAME}:${IMAGE_TAG}-builder --target builder .

build-dev-image: clean
	export DOCKER_CONTENT_TRUST=1
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg UV_VERSION=${UV_VERSION} --file docker/Dockerfile --tag ${APP_NAME}:${IMAGE_TAG}-dev --target development .

build-image: clean
	export DOCKER_CONTENT_TRUST=1
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg UV_VERSION=${UV_VERSION} --file docker/Dockerfile --tag ${APP_NAME}:${IMAGE_TAG} --target production .

# ---------------------------------------------------------------------------- #
#               ------- Docker Compose ------
# ---------------------------------------------------------------------------- #
compose-up:
	export IMAGE_TAG=${IMAGE_TAG}
	docker compose -f docker/compose.yaml up -d

compose-down:
	export IMAGE_TAG=${IMAGE_TAG}
	docker compose -f docker/compose.yaml down -v

# ---------------------------------------------------------------------------- #
#               ------- Docker Create ------
# ---------------------------------------------------------------------------- #
create-container:
	docker create --env-file .env --name ${APP_NAME} ${APP_NAME}:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Docker Run ------
# ---------------------------------------------------------------------------- #
run-dev-container:
	docker run --env-file .env --name ${APP_NAME} --rm  --volume /mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME}:/mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME} ${APP_NAME}:${IMAGE_TAG}-dev

run-container:
	docker run --env-file .env --name ${APP_NAME} --rm  --volume /mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME}:/mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME} ${APP_NAME}:${IMAGE_TAG}

run-container-detach:
	docker run --detach --env-file .env --name ${APP_NAME} --rm  --volume /mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME}:/mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME} ${APP_NAME}:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Docker Run Debug ------
# ---------------------------------------------------------------------------- #
run-container-pdb:
	docker run --entrypoint python --env-file .env --interactive --name ${APP_NAME}-debug --rm  --tty --volume /mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME}:/mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME} ${APP_NAME}:${IMAGE_TAG} -m pdb -m ${APP_NAME_SNAKE}.main

run-container-debugpy:
	docker run --env DEBUGPY=true --env-file .env --name ${APP_NAME}-debug --publish 5678:5678 --rm --volume $(shell pwd)/src:/app/src --volume /mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME}:/mnt/naos_share/${CUSTOMER_NAME}/${APP_NAME} ${APP_NAME}:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Dive ------
# ---------------------------------------------------------------------------- #
dive-image:
	dive ${APP_NAME}:${IMAGE_TAG}

dive-image-ci:
	CI=true dive ${APP_NAME}:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Grype ------
# ---------------------------------------------------------------------------- #
grype-repo:
	grype .

grype-builder-image:
	grype ${APP_NAME}:${IMAGE_TAG}-builder --scope all-layers

grype-dev-image:
	grype ${APP_NAME}:${IMAGE_TAG}-dev --scope all-layers

grype-image:
	grype ${APP_NAME}:${IMAGE_TAG} --scope all-layers

grype-update:
	grype db update

# ---------------------------------------------------------------------------- #
#               ------- Trivy ------
# ---------------------------------------------------------------------------- #
trivy-clean:
	trivy clean --all

trivy-repo:
	trivy repository --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln .

trivy-builder-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln ${APP_NAME}:${IMAGE_TAG}-builder

trivy-dev-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln ${APP_NAME}:${IMAGE_TAG}-dev

trivy-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln ${APP_NAME}:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Dockle ------
# ---------------------------------------------------------------------------- #
dockle-image-security:
	dockle ${APP_NAME}:${IMAGE_TAG}

dockle-builder-image-security:
	dockle ${APP_NAME}:${IMAGE_TAG}-builder

# ---------------------------------------------------------------------------- #
#               ------- Checkov ------
# ---------------------------------------------------------------------------- #
checkov:
	checkov --config-file checkov.yaml

# ---------------------------------------------------------------------------- #
#               ------- Kubernetes ------
# ---------------------------------------------------------------------------- #
pod-pdb:
	kubectl run ${APP_NAME}-debug --image=${APP_NAME}:${IMAGE_TAG} --attach --restart=Never --stdin --tty --command -- python -m pdb -m ${APP_NAME_SNAKE}.main

pod-debugpy:
	kubectl run ${APP_NAME}-debug --image=${APP_NAME}:${IMAGE_TAG} --env="DEBUGPY=true" --port=5678 --restart=Never
	kubectl port-forward pod/${APP_NAME}-debug 5678:5678

# ---------------------------------------------------------------------------- #
#               ------- Other ------
# ---------------------------------------------------------------------------- #
clean:
	find . -type f -name '*.py[cod]' | xargs rm -rf
	find . -type d -name 'control' | xargs rm -rf
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '.mypy_cache' | xargs rm -rf
	find . -type d -name '.pytest_cache' | xargs rm -rf
	find . -type d -name '.ruff_cache' | xargs rm -rf
