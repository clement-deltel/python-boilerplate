# ---------------------------------------------------------------------------- #
#               ------- VARIABLES ------
# ---------------------------------------------------------------------------- #
IMAGE_TAG=$(shell cz version --project)

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
	uv run pre-commit install --install-hooks
	source .venv/bin/activate

init-test:
	uv sync --frozen --group test --no-default-groups
	source .venv/bin/activate

init-from-scratch:
	uv init --build-backend uv --managed-python --name app-name --python 3.11.11 --vcs git
	uv sync
	source .venv/bin/activate

init-auto-activate:
	pyenv install 3.11.11
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/3.11.11_app-name
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/3.11.11/envs/3.11.11_app-name
	pyenv local 3.11.11_app-name

auto-activate:
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/3.11.11_app-name
	ln -s $(shell pwd)/.venv ~/.pyenv/versions/3.11.11/envs/3.11.11_app-name
	pyenv local 3.11.11_app-name

# ---------------------------------------------------------------------------- #
#               ------- Requirements ------
# ---------------------------------------------------------------------------- #
requirement:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt

requirement-dev:
	uv export --format requirements-txt --group dev --group lint --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt

requirement-test:
	uv export --format requirements-txt --group test --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt

requirement-all:
	uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
	uv export --format requirements-txt --group dev --group lint --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt
	uv export --format requirements-txt --group test --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt

# ---------------------------------------------------------------------------- #
#               ------- Code ------
# ---------------------------------------------------------------------------- #
run:
	python -m src.app_name.main

debug:
	export PYTHONPATH=$(pwd)
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
	pre-commit install --install-hooks

hook-run:
	pre-commit run --all-files

# ---------------------------------------------------------------------------- #
#               ------- Image ------
# ---------------------------------------------------------------------------- #
get-tag:
	echo "export IMAGE_TAG=${IMAGE_TAG}"

build-image: clean
	docker build --file docker/Dockerfile --tag app-name:${IMAGE_TAG} .

pull-image:
	docker pull app-name:${IMAGE_TAG}

push-image:
	docker push app-name:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Container ------
# ---------------------------------------------------------------------------- #
create-container:
	docker create --env-file .env --name app-name app-name:${IMAGE_TAG}

run-container:
	docker run --env-file .env --name app-name --rm app-name:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Dive ------
# ---------------------------------------------------------------------------- #
dive-image:
	dive app-name:${IMAGE_TAG}

dive-image-ci:
	CI=true dive app-name:${IMAGE_TAG}

# ---------------------------------------------------------------------------- #
#               ------- Scan ------
# ---------------------------------------------------------------------------- #
scan-repo:
	trivy repository --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln .

scan-image:
	trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vul app-name:${IMAGE_TAG}

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
