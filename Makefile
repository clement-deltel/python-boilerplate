# --------------------------------------------------------------------------- #
#               ------- Initialization ------
# --------------------------------------------------------------------------- #
pre-requisites:
	curl -fLSs https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
	curl -fLSs https://astral.sh/uv/install.sh | sh
	brew install ls-lint

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

auto-activate:
    pyenv install 3.11.8
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8_app
	ln -s $(pwd)/.venv ~/.pyenv/versions/3.11.8/envs/3.11.8_app
	pyenv local 3.11.8_app

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
	docker pull app:latest

# --------------------------------------------------------------------------- #
#               ------- Container ------
# --------------------------------------------------------------------------- #
create-container:
	docker create --env-file .env --name app app:latest

run-container:
	docker run --env-file .env --name app --rm app:latest

# --------------------------------------------------------------------------- #
#               ------- Other ------
# --------------------------------------------------------------------------- #
merge-request:
	tokei
	uv tree --no-default-groups
	trivy image --image-config-scanners misconfig,secret --scanners vuln,secret app:latest

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.mypy_cache' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.ruff_cache' -delete
