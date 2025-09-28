# ---------------------------------------------------------------------------- #
#               ------- VARIABLES ------
# ---------------------------------------------------------------------------- #

# User defined
PYTHON_TARGET_VERSION:=3.11.13

UV_SOURCE_VERSION:=0.8.18
UV_TARGET_VERSION:=0.8.18

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
	uv init --build-backend uv --managed-python --name app-name --python ${PYTHON_VERSION} --vcs git
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
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/${PYTHON_VERSION}_customer_app-name
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/${PYTHON_VERSION}/envs/${PYTHON_VERSION}_customer_app-name
	pyenv local ${PYTHON_VERSION}_customer_app-name

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
	app_name

run-module:
	python -m app_name.main

run-program:
	python src/app_name/main.py

run-uv:
	uv run app_name

# ---------------------------------------------------------------------------- #
#               ------- Telemetry ------
# ---------------------------------------------------------------------------- #
init-telemetry:
	uv run opentelemetry-bootstrap -a requirements | uv pip install --requirement -

run-telemetry: init-telemetry
	opentelemetry-instrument \
	--service_name app-name \
	--logs_exporter console \
	--traces_exporter console \
    --metrics_exporter console \
	python src/app_name/main.py

# ---------------------------------------------------------------------------- #
#               ------- Debug & Test ------
# ---------------------------------------------------------------------------- #
debug:
	python -m pdb src/app_name/main.py

test:
	python -m pytest --color=yes --durations=5 --verbose --config-file=test/pytest.ini test/

coverage:
	coverage run --rcfile=pyproject.toml -m pytest --color=yes --verbose --config-file=test/pytest.ini
	coverage report --show-missing

# ---------------------------------------------------------------------------- #
#               ------- Pre-commit Hooks ------
# ---------------------------------------------------------------------------- #
hook-install:
	prek install --install-hooks

hook-run:
	prek run --all-files

# ---------------------------------------------------------------------------- #
#               ------- Image ------
# ---------------------------------------------------------------------------- #
get-tag:
	echo "export IMAGE_TAG=${IMAGE_TAG}"

build-image: clean
	export DOCKER_CONTENT_TRUST=1
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg UV_VERSION=${UV_VERSION} --file docker/Dockerfile --tag app-name:${IMAGE_TAG} .

build-builder-image: clean
	export DOCKER_CONTENT_TRUST=1
	docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} --build-arg UV_VERSION=${UV_VERSION} --file docker/Dockerfile --tag app-name:${IMAGE_TAG}-builder --target builder .

pull-image:
	docker pull app-name:${IMAGE_TAG}

push-image:
	docker push app-name:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Container ------
# ---------------------------------------------------------------------------- #
create-container:
	docker create --env-file .env --name app-name app-name:${IMAGE_TAG}

debug-container:
	python -m pdb .venv/lib/python3.11/site-packages/app_name/main.py

run-container:
	docker run --env-file .env --name app-name --rm app-name:${IMAGE_TAG}

run-container-detach:
	docker run --detach --env-file .env --name app-name --rm app-name:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Dive ------
# ---------------------------------------------------------------------------- #
dive-image:
	dive app-name:${IMAGE_TAG}

dive-image-ci:
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

trivy-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vul app-name:${IMAGE_TAG}

trivy-builder-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vul app-name:${IMAGE_TAG}-builder

# ---------------------------------------------------------------------------- #
#               ------- Dockle ------
# ---------------------------------------------------------------------------- #
dockle-image-security:
	dockle app-name:${IMAGE_TAG}

dockle-builder-image-security:
	dockle app-name:${IMAGE_TAG}-builder

# ---------------------------------------------------------------------------- #
#               ------- Checkov ------
# ---------------------------------------------------------------------------- #
checkov:
	checkov --config-file checkov.yaml

# ---------------------------------------------------------------------------- #
#               ------- Other ------
# ---------------------------------------------------------------------------- #
clean:
	find . -type f -name '*.pyc' | xargs rm -rf
	find . -type d -name 'control' | xargs rm -rf
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '.mypy_cache' | xargs rm -rf
	find . -type d -name '.pytest_cache' | xargs rm -rf
	find . -type d -name '.ruff_cache' | xargs rm -rf
