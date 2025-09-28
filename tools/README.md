# Tools Guidelines <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Source Code](#source-code)
  - [uv](#uv)
  - [ruff](#ruff)
  - [ty](#ty)
  - [prek](#prek)
  - [gitleaks](#gitleaks)
  - [ls-lint](#ls-lint)
  - [varlock](#varlock)
- [Performance](#performance)
  - [cProfile](#cprofile)
- [Containerization](#containerization)
  - [docker](#docker)
  - [hadolint](#hadolint)
  - [dive](#dive)
    - [dockle](#dockle)
  - [grype](#grype)
  - [trivy](#trivy)
- [Cloud](#cloud)
  - [checkov](#checkov)
- [Documentation](#documentation)
  - [tokei](#tokei)
  - [csv2md](#csv2md)
  - [readme-generator-for-helm](#readme-generator-for-helm)

## Introduction

This document gives general guidelines and command examples for all the tools that I use when it comes to code in Python.

## Source Code

### uv

Here are useful commands to manage the Python virtual environment and the dependencies using [uv](https://docs.astral.sh/uv) ([source code](https://github.com/astral-sh/uv)). Do you want to:

Ensures that all project dependencies (listed in `pyproject.toml`) are installed and up-to-date with the lockfile `uv.lock`?

```bash
uv sync
```

Upgrade all project dependencies?

```bash
uv sync --upgrade
```

Visualize the dependency tree?

```bash
uv tree --no-default-groups
```

Add a new dependency...

- for the project?

```bash
uv add <package>
```

- for **development** purposes only?

```bash
uv add --group dev <package>
```

- for **test** purposes only?

```bash
uv add --group test <package>
```

Remove a dependency...

- for the project?

```bash
uv remove <package>
```

- for **development** purposes only?

```bash
uv remove --group dev <package>
```

- for **test** purposes only?

```bash
uv remove --group test <package>
```

Upgrade a dependency...

- without specifying a version?

```bash
uv sync --upgrade-package <package>
```

- specifying a version?

```bash
uv sync --upgrade-package <package>==<version>
```

Export dependencies and update requirements files...

- as a **user** and for the project?

```bash
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
```

- as a **developer**?

```bash
uv export --format requirements-txt --group dev --group lint --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt
```

- as a **QA engineer**?

```bash
uv export --format requirements-txt --group test --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt
```

- Update the tool itself?

```bash
uv self update
prek autoupdate --repo https://github.com/astral-sh/uv-pre-commit
```

### ruff

Here are useful commands to lint and format code using [ruff](https://docs.astral.sh/ruff) ([source code](https://github.com/astral-sh/ruff)). Do you want to:

Lint all files in the current directory, and fix any fixable errors?

```bash
ruff check --fix
```

Format all files in the current directory?

```bash
ruff format
```

Format a single file?

```bash
ruff format path/to/file.py
```

### ty

Here are useful commands to check variable type using [ty](https://github.com/astral-sh/ty) ([source code](https://github.com/astral-sh/ty)). Do you want to:

Check all files in the current directory?

```bash
ty check
```

### prek

Here are useful commands to manage the git hooks using [prek](https://prek.j178.dev) ([source code](https://github.com/j178/prek)). Do you want to:

Install hooks?

```bash
prek install --install-hooks
```

Run all hooks on all the files in the repository?

```bash
prek run --all-files
```

Run all hooks on a specific file in the repository?

```bash
prek run --files <path/to/file>
```

Produce hook output independent of success?

```bash
prek run --all-files --verbose
```

Run a specific hook?

```bash
prek run <hook-id> --all-files --verbose
```

Auto-update hooks config to the latest repos' versions?

```bash
prek autoupdate
```

Uninstall hooks?

```bash
prek uninstall
```

### gitleaks

Here are useful commands to detect potential secret leaks using [gitleaks](https://gitleaks.io) ([source code](https://github.com/gitleaks/gitleaks)). Do you want to:

Scan all the commits?

```bash
gitleaks git --redact --verbose
```

### ls-lint

Here are useful commands to ensure consistent project filesystem structure using [ls-lint](https://ls-lint.org/) ([source code](https://github.com/loeffel-io/ls-lint)). Do you want to:

Check the project filesystem structure?

```bash
ls-lint
```

### varlock

Here are useful commands to ensure consistent .env structure by adding @env-spec decorator comments, using [varlock](https://varlock.dev/) ([source code](https://github.com/dmno-dev/varlock)). Do you want to:

Check the .env file structure:

```bash
varlock load
```

## Performance

### cProfile

Here are useful commands to analyze the code performance and identify bottlenecks using [cProfile](https://docs.python.org/3/library/profile.html).

- Set the environment variable **PROFILING** to "true" to enable this functionality.
- Once you run the application, it should generate a report named "{date}_{app}.prof" to the output path by the time it finishes
- Open the report with a text editor or visualize it using [snakeviz](https://jiffyclub.github.io/snakeviz):

```bash
snakeviz {date}_{app}.prof
```

## Containerization

### docker

Here are useful commands to manage the Docker configuration. Do you want to:

- Test the `dockerignore` file?

```bash
rsync --archive --dry-run --exclude-from .dockerignore --verbose . /dev/shm
```

### hadolint

Here are useful commands to lint the Dockerfile using [hadolint](https://github.com/hadolint/hadolint) ([source code](https://github.com/hadolint/hadolint)). Do you want to:

Apply best practices on your Dockerfile?

```bash
hadolint docker/Dockerfile
```

### dive

Here are useful commands to explore image layers using [dive](https://github.com/wagoodman/dive) ([source code](https://github.com/wagoodman/dive)). Do you want to:

Explore image layers?

```bash
dive app-name:latest
```

Analyze image efficiency in CI mode?

```bash
CI=true dive app-name:latest
```

#### dockle

Here are useful commands to detect potential security flaws of the Docker image using [dockle](https://containers.goodwith.tech/) ([source code](https://github.com/goodwithtech/dockle)). Do you want to:

Analyze image security?

```bash
dockle app-name:latest
```

### grype

Here are useful commands to scan an image using [grype](https://github.com/anchore/grype) ([source code](https://github.com/anchore/grype)). Do you want to:

Find vulnerabilities in an image?

```bash
grype app-name:latest --scope all-layers
```

### trivy

Here are useful commands to scan an image using [trivy](https://trivy.dev/latest) ([source code](https://github.com/aquasecurity/trivy)). Do you want to:

Find vulnerabilities, misconfigurations, secrets in an image?

```bash
trivy image --image-config-scanners misconfig,secret --scanners vuln,secret app-name:latest
```

## Cloud

### checkov

Here are useful commands to prevent cloud misconfigurations and find vulnerabilities using [checkov](https://www.checkov.io) ([source code](https://github.com/bridgecrewio/checkov)). Do you want to:

Run the tool on the repository?

```bash
checkov --config-file checkov.yaml
```

## Documentation

### tokei

Here are useful commands to generate some code statistics and add them to the README using [tokei](https://github.com/XAMPPRocky/tokei).

- Once installed with your method of choice, run the following command at the root of the repository:

```bash
tokei .
```

- Copy the table from stdout to `README.md` in a code block

### csv2md

Here are useful commands to manage the README documentation using [csv2md](https://pypi.org/project/csv2md). Do you want to:

Easily update the Markdown table of environment variables?

- Update the file `doc/env.csv`
- Generate the corresponding Markdown table:

```bash
python -m csv2md doc/env.csv
```

- Copy the table from stdout to `README.md`

### readme-generator-for-helm

Here are useful commands to manage the Helm chart documentation using [readme-generator-for-helm](https://github.com/bitnami/readme-generator-for-helm). Do you want to:

Update the README.md in the *helm_chart* directory?

```bash
readme-generator --values helm_chart/values.yaml --readme helm_chart/README.md
```

> Note: For any documentation related contribution, please use a spell checking tool like [Grammarly](https://www.grammarly.com) to avoid typographical and any other type of errors.
