# --------------------------------------------------------------------------- #
#               ------- VARIABLES ------
# --------------------------------------------------------------------------- #
IMAGE_TAG=app-$(shell cz version --project)

# --------------------------------------------------------------------------- #
#               ------- Initialization ------
# --------------------------------------------------------------------------- #
pre-requisites:
	curl -fLSs https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
	curl -fLSs https://astral.sh/uv/install.sh | sh
	brew install ls-lint
	brew install dmno-dev/tap/varlock

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
	uv init --build-backend hatchling --managed-python --name app --python 3.11.8 --vcs git
	uv sync
	source .venv/bin/activate

init-auto-activate:
	pyenv install 3.11.8
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8_app
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8/envs/3.11.8_app
	pyenv local 3.11.8_app

auto-activate:
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8_app
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8/envs/3.11.8_app
	pyenv local 3.11.8_app

# --------------------------------------------------------------------------- #
#               ------- Requirements ------
# --------------------------------------------------------------------------- #
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

# --------------------------------------------------------------------------- #
#               ------- Code ------
# --------------------------------------------------------------------------- #
run:
	python -m src.app.main

debug:
	export PYTHONPATH=$(pwd)
	python -m pdb src/app/main.py

test:
	python -m pytest --color=yes --durations=5 --verbose --config-file=test/pytest.ini test/

coverage:
	coverage run --rcfile=pyproject.toml -m pytest --color=yes --verbose --config-file=test/pytest.ini
	coverage report --show-missing

# --------------------------------------------------------------------------- #
#               ------- Image ------
# --------------------------------------------------------------------------- #
build-image:
	docker build --file docker/Dockerfile --tag app .

pull-image:
	docker pull app:${IMAGE_TAG}

push-image:
	docker push app:${IMAGE_TAG}

# --------------------------------------------------------------------------- #
#               ------- Container ------
# --------------------------------------------------------------------------- #
create-container:
	docker create --env-file .env --name app app:${IMAGE_TAG}

run-container:
	docker run --env-file .env --name app --rm app:${IMAGE_TAG}

# --------------------------------------------------------------------------- #
#               ------- Other ------
# --------------------------------------------------------------------------- #
clean:
	find . -type f -name '*.pyc' | xargs rm -rf
	find . -type d -name 'control' | xargs rm -rf
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '.mypy_cache' | xargs rm -rf
	find . -type d -name '.pytest_cache' | xargs rm -rf
	find . -type d -name '.ruff_cache' | xargs rm -rf

merge-request:
	tokei
	uv tree --no-default-groups
	trivy image --image-config-scanners misconfig,secret --scanners vuln,secret app:${IMAGE_TAG}
