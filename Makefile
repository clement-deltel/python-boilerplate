pre-requisites:
  curl -fLSs https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
  curl -fLSs https://astral.sh/uv/install.sh | sh
  brew install ls-lint

init:
  uv sync --no-default-groups --no-install-project
  source .venv/bin/activate

init-dev:
  uv sync --no-install-project
  source .venv/bin/activate

init-test:
  uv sync --group test --no-default-groups --no-install-project
  source .venv/bin/activate

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

build-container:
  docker build --file docker/Dockerfile --tag app .

create-container:
  docker create --env-file .env --name app app:latest

pull-container:
  docker pull app:latest

run-container:
  docker run --env-file .env --name app --rm app:latest

clean:
  find . -type f -name '*.pyc' -delete
  find . -type d -name '__pycache__' -delete
