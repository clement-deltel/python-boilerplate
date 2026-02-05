# https://github.com/casey/just
# Useful commands
# just --dry-run         # Show commands without executing them
# just --evaluate        # Evaluate and print all variables
# just --list            # List all available recipes in alphabetical order
# just --list --unsorted # List all available recipes in order of appearance

# Choose a recipe to run in interactive mode
[private]
default:
    @just --choose

# ---------------------------------------------------------------------------- #
#               ------- VARIABLES ------
# ---------------------------------------------------------------------------- #
# User defined

customer := "customer"
name := "app-name"
name_snake := "app_name"

# Generated

image_tag := `cz version --project`
python_version := `uv run -qq python --version | sed 's/Python //'`
uv_version := `uv self version | sed 's/uv //'`

# ---------------------------------------------------------------------------- #
#               ------- Initialization ------
# ---------------------------------------------------------------------------- #

# Install application pre-requisites
[group("initialization")]
pre-requisites:
    curl -fLSs https://astral.sh/uv/install.sh | sh
    curl -fLSs https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
    brew install charmbracelet/tap/freeze gitleaks git-cliff hadolint ls-lint onefetch tokei varlock

# Initialize environment as a user
[group("initialization")]
[linux]
init:
    uv sync --frozen --no-default-groups
    source .venv/bin/activate

# Initialize environment as a developer
[group("initialization")]
[linux]
init-dev:
    uv sync --frozen
    uv run pre-commit install --install-hooks
    source .venv/bin/activate

# Initialize environment as a tester
[group("initialization")]
[linux]
init-test:
    uv sync --frozen --group test --no-default-groups
    source .venv/bin/activate

# Initialize environment as a new application
[group("initialization")]
[linux]
init-from-scratch:
    uv init --build-backend uv --managed-python --name {{ name }} --python {{ python_version }} --vcs git
    uv sync
    source .venv/bin/activate

# Initialize environment as a user
[group("initialization")]
[windows]
init:
    uv venv --python {{ python_version }}
    uv pip install --editable .
    .venv/Scripts/activate

# Initialize environment as a developer
[group("initialization")]
[windows]
init-dev:
    uv venv --python {{ python_version }}
    uv pip install --group dev --group lint --editable .
    .venv/Scripts/activate

# ---------------------------------------------------------------------------- #
#               ------- Pyenv ------
# ---------------------------------------------------------------------------- #

# Install Python version using pyenv
[group("pyenv")]
init-pyenv:
    pyenv install {{ python_version }}

# Create symlinks to have venv auto-activation with pyenv
[group("pyenv")]
activate:
    ln -s ${pwd}/.venv ~/.pyenv/versions/{{ python_version }}_{{ customer }}_{{ name }}
    ln -s ${pwd}/.venv ~/.pyenv/versions/{{ python_version }}/envs/{{ python_version }}_{{ customer }}_{{ name }}
    pyenv local {{ python_version }}_{{ customer }}_{{ name }}

# Initialize environment as a developer and create symlinks to have venv auto-activation with pyenv
[group("pyenv")]
init-activate: init-dev activate

# ---------------------------------------------------------------------------- #
#               ------- Python ------
# ---------------------------------------------------------------------------- #
# just update-patch 3.11.15
# just update-minor 3.12.0

# Update Python version in .pre-commit-config.yaml
[arg("target", pattern='^([23])\.(\d{1,2})\.(\d{1,2})$')]
[group("python")]
update-pre-commit target="3.11.14":
    #!/usr/bin/env bash
    SOURCE=`uv run -qq python --version | sed 's/Python //' | cut -d. -f1-2`
    TARGET=`echo {{ target }} | cut -d. -f1-2`
    sed -i "s/${SOURCE}/${TARGET}/g" .pre-commit-config.yaml
    git add .pre-commit-config.yaml

# Update Python version in pyproject.toml
[arg("target", pattern='^([23])\.(\d{1,2})\.(\d{1,2})$')]
[group("python")]
update-pyproject target="3.11.14":
    #!/usr/bin/env bash
    SOURCE=`uv run -qq python --version | sed 's/Python //' | cut -d. -f1-2`
    TARGET=`echo {{ target }} | cut -d. -f1-2`
    sed -i "s/${SOURCE}\"/${TARGET}\"/g" pyproject.toml
    SOURCE:=`uv run -qq python --version | sed 's/Python //' | cut -d. -f1-2 | tr -d .`
    TARGET=`echo {{ target }} | cut -d. -f1-2 | tr -d .` && sed -i "s/${SOURCE}/${TARGET}/g" pyproject.toml
    git add pyproject.toml

# Update Python version, recreate venv, and sync dependencies
[arg("target", pattern='^([23])\.(\d{1,2})\.(\d{1,2})$')]
[group("python")]
update-python target="3.11.14":
    @rm -f .python-version || true
    @rm -rf .venv
    uv python install {{ target }}
    uv sync --frozen
    sed -i "s/{{ python_version }}/{{ target }}/g" docker/Dockerfile docker/alpine.Dockerfile docker/wheel.Dockerfile Justfile
    git add docker/Dockerfile docker/alpine.Dockerfile docker/wheel.Dockerfile Justfile

# Update Python version PATCH digit everywhere, recreate venv, sync dependencies, and create symlinks for pyenv venv auto-activation
[arg("target", pattern='^([23])\.(\d{1,2})\.(\d{1,2})$')]
[group("python")]
update-patch target="3.11.14": (update-python target) activate

# update Python version MINOR digit everywhere, recreate venv, sync dependencies, and create symlinks for pyenv venv auto-activation
[arg("target", pattern='^([23])\.(\d{1,2})\.(\d{1,2})$')]
[group("python")]
update-minor target="3.11.14": (update-python target) update-pre-commit update-pyproject activate

# ---------------------------------------------------------------------------- #
#               ------- Uv ------
# ---------------------------------------------------------------------------- #
# https://docs.astral.sh/uv

# Build application
[group("uv")]
build:
    uv sync

# Check for uv updates
[group("uv")]
uv-check:
    uv self update --dry-run

# Update uv version in files and self-update uv
[arg("source", pattern='^(\d)\.(\d{1,2})\.(\d{1,2})$')]
[group("uv")]
uv-update source="0.9.30":
    uv self update
    sed -i "s/{{ source }}/{{ uv_version }}/g" docker/Dockerfile docker/alpine.Dockerfile docker/wheel.Dockerfile .pre-commit-config.yaml Justfile pyproject.toml
    git add docker/Dockerfile docker/alpine.Dockerfile docker/wheel.Dockerfile .pre-commit-config.yaml Justfile pyproject.toml

# ---------------------------------------------------------------------------- #
#               ------- Dependencies ------
# ---------------------------------------------------------------------------- #

# Update all dependency groups
[group("dependencies")]
update-groups:
    # dev
    uv sync --upgrade-package commitizen
    uv sync --upgrade-package csv2md
    uv sync --upgrade-package howdoi
    uv sync --upgrade-package prek
    uv sync --upgrade-package pyscn
    uv sync --upgrade-package snakeviz
    # lint
    uv sync --upgrade-package checkov
    uv sync --upgrade-package gitlint
    uv sync --upgrade-package isort
    uv sync --upgrade-package pyright
    uv sync --upgrade-package pyupgrade
    uv sync --upgrade-package refurb
    uv sync --upgrade-package ruff
    uv sync --upgrade-package ty
    uv sync --upgrade-package yamllint
    # observability
    uv sync --upgrade-package opentelemetry-distro
    # test
    uv sync --upgrade-package coverage
    uv sync --upgrade-package pytest
    uv sync --upgrade-package pytest-mock
    # typing
    # uv sync --upgrade-package pandas-stubs
    uv sync --upgrade-package types-requests
    git add uv.lock

# Update all dependency groups as well as pre-commit hooks
[group("dependencies")]
update: update-groups hook-update

# ---------------------------------------------------------------------------- #
#               ------- Run ------
# ---------------------------------------------------------------------------- #

# Run application
[group("run")]
run:
    {{ name_snake }}

# Run application using module
[group("run")]
run-module:
    python -m {{ name_snake }}.main

# Run application program directly
[group("run")]
run-program:
    python src/{{ name_snake }}/main.py

# Run application using uv
[group("run")]
run-uv:
    uv run {{ name_snake }}

# ---------------------------------------------------------------------------- #
#               ------- Debug ------
# ---------------------------------------------------------------------------- #

# Run application in debug mode with pdb
[group("debug")]
debug:
    python -m pdb -m {{ name_snake }}.main

# Run application program in debug mode with pdb
[group("debug")]
debug-program:
    python -m pdb src/{{ name_snake }}/main.py

# Run application program in debug mode with pdb from venv
[group("debug")]
debug-program-venv:
    PYTHON_SHORT_VERSION=`uv run -qq python --version | sed 's/Python //' | cut -d. -f1-2` && python -m pdb .venv/lib/python${PYTHON_SHORT_VERSION}/site-packages/{{ name_snake }}/main.py

# ---------------------------------------------------------------------------- #
#               ------- Lint ------
# ---------------------------------------------------------------------------- #

# Lint code with ruff and fix issues
[group("lint")]
lint:
    ruff check --fix

# Lint repository directories with ls-lint
[group("lint")]
lint-dir:
    ls-lint

# Lint environment file with varlock
[group("lint")]
lint-env:
    varlock load

# ---------------------------------------------------------------------------- #
#               ------- Test ------
# ---------------------------------------------------------------------------- #

# Run tests with pytest
[group("test")]
test:
    python -m pytest --color=yes --durations=5 --verbose --config-file=test/pytest.ini test/

# Run coverage
[group("test")]
coverage:
    coverage run --rcfile=pyproject.toml -m pytest --color=yes --verbose --config-file=test/pytest.ini
    coverage report --show-missing

# ---------------------------------------------------------------------------- #
#               ------- Telemetry ------
# ---------------------------------------------------------------------------- #
# https://opentelemetry.io/

# Initialize telemetry dependencies
[group("telemetry")]
init-telemetry:
    uv run opentelemetry-bootstrap -a requirements | uv pip install --requirement -

# Run application program with OpenTelemetry instrumentation
[group("telemetry")]
run-telemetry: init-telemetry
    opentelemetry-instrument \
    --service_name {{ name }} \
    --logs_exporter console \
    --traces_exporter console \
    --metrics_exporter console \
    python src/{{ name_snake }}/main.py

# ---------------------------------------------------------------------------- #
#               ------- Pre-commit Hooks ------
# ---------------------------------------------------------------------------- #
# https://github.com/j178/prek

# Install pre-commit hooks
[group("hooks")]
hook-install:
    prek install --install-hooks

# Run pre-commit hooks against all files
[group("hooks")]
hook-run:
    prek run --all-files

# Update pre-commit hooks and stage config
[group("hooks")]
hook-update:
    prek auto-update
    git add .pre-commit-config.yaml

# ---------------------------------------------------------------------------- #
#               ------- Pyscn ------
# ---------------------------------------------------------------------------- #
# https://github.com/ludo-technologies/pyscn

# Run pyscn analysis
[group("pyscn")]
pyscn-run:
    pyscn analyze src/

# ---------------------------------------------------------------------------- #
#               ------- Docker ------
# ---------------------------------------------------------------------------- #
# just build-image
# just build-image builder -builder
# just build-image distroless -distroless

# Get Docker image tag
[group("docker")]
get-tag:
    @echo "export IMAGE_TAG={{ image_tag }}"

# Build Docker image. Targets: builder, distroless. Tag suffixes: -builder, -distroless
[group("docker"), arg("target", pattern='^(production|builder|distroless)$'), arg("tag_suffix", pattern='^(-builder|-distroless)?$')]
build-image target="production" tag_suffix="" $DOCKER_CONTENT_TRUST="1": clean
    docker build --build-arg PYTHON_VERSION={{ python_version }} --build-arg UV_VERSION=0.9.30 --file docker/Dockerfile --tag {{ name }}:{{ image_tag }}{{ tag_suffix }} --target {{ target }} .

# Pull Docker image
[group("docker")]
pull-image:
    docker pull {{ name }}:{{ image_tag }}

# Push Docker image
[group("docker")]
push-image:
    docker push {{ name }}:{{ image_tag }}

# Test Docker container healthcheck
[group("docker")]
run-healthcheck:
    docker exec {{ name }} python healthcheck.py

# ---------------------------------------------------------------------------- #
#               ------- Docker Create ------
# ---------------------------------------------------------------------------- #

# Create Docker production container
[group("docker")]
create-container:
    docker create --env-file .env --name {{ name }} {{ name }}:{{ image_tag }}

# ---------------------------------------------------------------------------- #
#               ------- Docker Run ------
# ---------------------------------------------------------------------------- #
# just run-container
# just run-container --detach
# just run-container --tag-suffix -distroless

# Run Docker container. Tag suffixes: -builder, -distroless
[group("docker"), arg("tag_suffix", long="tag-suffix", pattern='^(-builder|-distroless)?$')]
run-container detach="" tag_suffix="":
    docker run {{ detach }} --env-file .env --name {{ name }} --rm  --volume /mnt/naos_share/{{ customer }}/{{ name }}:/mnt/naos_share/{{ customer }}/{{ name }} {{ name }}:{{ image_tag }}{{ tag_suffix }}

# ---------------------------------------------------------------------------- #
#               ------- Docker Run Debug ------
# ---------------------------------------------------------------------------- #

# Run Docker production container in debug mode with pdb
[group("docker")]
run-container-pdb:
    docker run --entrypoint python --env-file .env --interactive --name {{ name }}-debug --rm  --tty --volume /mnt/naos_share/{{ customer }}/{{ name }}:/mnt/naos_share/{{ customer }}/{{ name }} {{ name }}:{{ image_tag }} -m pdb -m {{ name_snake }}.main

# Run Docker production container in debug mode with debugpy
[group("docker")]
run-container-debugpy:
    docker run --env DEBUGPY=true --env-file .env --name {{ name }}-debug --publish 5678:5678 --rm --volume ${pwd}/src:/app/src --volume /mnt/naos_share/{{ customer }}/{{ name }}:/mnt/naos_share/{{ customer }}/{{ name }} {{ name }}:{{ image_tag }}

# ---------------------------------------------------------------------------- #
#               ------- Docker Compose ------
# ---------------------------------------------------------------------------- #

# Bring up Docker Compose services
[group("docker-compose")]
compose-up $IMAGE_TAG=`cz version --project`:
    docker compose -f docker/compose.yaml up -d

# Bring down Docker Compose services
[group("docker-compose")]
compose-down $IMAGE_TAG=`cz version --project`:
    docker compose -f docker/compose.yaml down -v

# ---------------------------------------------------------------------------- #
#               ------- Dive ------
# ---------------------------------------------------------------------------- #
# https://github.com/wagoodman/dive

# Dive into Docker image
[group("dive")]
dive:
    dive {{ name }}:{{ image_tag }}

# Dive into Docker image in CI mode
[group("dive")]
dive-ci:
    CI=true dive {{ name }}:{{ image_tag }}

# ---------------------------------------------------------------------------- #
#               ------- Grype ------
# ---------------------------------------------------------------------------- #
# https://github.com/anchore/grype
# just grype
# just grype -builder
# just grype -distroless

# Run grype vulnerability scan on image. Tag suffixes: -builder, -distroless
[group("grype"), arg("tag_suffix", pattern='^(-builder|-distroless)?$')]
grype tag_suffix="":
    grype {{ name }}:{{ image_tag }}{{ tag_suffix }} --scope all-layers

# Run grype vulnerability scan on repository
[group("grype")]
grype-repo:
    grype .

# Update grype vulnerability database
[group("grype")]
grype-update:
    grype db update

# ---------------------------------------------------------------------------- #
#               ------- Trivy ------
# ---------------------------------------------------------------------------- #
# https://github.com/aquasecurity/trivy
# just trivy
# just trivy -builder
# just trivy -distroless

# Run trivy vulnerability scan on image. Tag suffixes: -builder, -distroless
[group("trivy"), arg("tag_suffix", pattern='^(-builder|-distroless)?$')]
trivy tag_suffix="":
    trivy image --image-config-scanners misconfig,secret --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln {{ name }}:{{ image_tag }}{{ tag_suffix }}

# Run trivy vulnerability scan on repository
[group("trivy")]
trivy-repo:
    trivy repository --misconfig-scanners dockerfile,helm,kubernetes --scanners misconfig,secret,vuln .

# Clean trivy cache
[group("trivy")]
trivy-clean:
    trivy clean --all

# ---------------------------------------------------------------------------- #
#               ------- Dockle ------
# ---------------------------------------------------------------------------- #
# https://github.com/goodwithtech/dockle
# just dockle
# just dockle -builder
# just dockle -distroless

# Run dockle security scan on image. Tag suffixes: -builder, -distroless
[group("dockle"), arg("tag_suffix", pattern='^(-builder|-distroless)?$')]
dockle tag_suffix="":
    dockle {{ name }}:{{ image_tag }}{{ tag_suffix }}

# ---------------------------------------------------------------------------- #
#               ------- Checkov ------
# ---------------------------------------------------------------------------- #
# https://github.com/bridgecrewio/checkov

# Run checkov security scan
[group("checkov")]
checkov:
    checkov --config-file checkov.yaml

# ---------------------------------------------------------------------------- #
#               ------- Kubernetes ------
# ---------------------------------------------------------------------------- #

# Run application pod in debug mode with pdb
[group("kubernetes")]
pod-pdb:
    kubectl run {{ name }}-debug --image {{ name }}:{{ image_tag }} --attach --restart Never --rm --stdin --tty --command -- python -m pdb -m {{ name_snake }}.main
    kubectl attach -it {{ name }}-debug --namespace default

# Run application pod in debug mode with debugpy
[group("kubernetes")]
pod-debugpy:
    kubectl run {{ name }}-debug --image {{ name }}:{{ image_tag }} --env "DEBUGPY=true" --port=5678 --restart=Never --rm
    kubectl port-forward pod/{{ name }}-debug 5678:5678 --namespace default

# Create Kubernetes Job object from CronJob
[group("kubernetes")]
job-create:
    kubectl create job --from cronjob/{{ name }} {{ name }}-debug --namespace default

# Delete Kubernetes Job object
[group("kubernetes")]
job-delete:
    kubectl delete job {{ name }}-debug --force --namespace default

# ---------------------------------------------------------------------------- #
#               ------- Helm ------
# ---------------------------------------------------------------------------- #

# Run Helm unittest
[group("helm")]
helm-test:
    helm unittest -o helm_chart/tests/helm_unittest_results.xml -t JUnit -v helm_chart/values.yaml helm_chart/

# ---------------------------------------------------------------------------- #
#               ------- Other ------
# ---------------------------------------------------------------------------- #

# Clean Python cache files and directories
[group("other")]
clean:
    @find . -type f -name '*.py[cod]' | xargs rm -rf
    @find . -type d -name 'control' | xargs rm -rf
    @find . -type d -name '__pycache__' | xargs rm -rf
    @find . -type d -name '.mypy_cache' | xargs rm -rf
    @find . -type d -name '.pytest_cache' | xargs rm -rf
    @find . -type d -name '.ruff_cache' | xargs rm -rf
