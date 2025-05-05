# Contributing <!-- omit in toc -->

🎉 First off, thanks for taking the time to contribute! 🎉

Anyone who wishes to contribute to this project - whether documentation, features, bug fixes, code cleanup, testing, or code reviews - is very much encouraged to do so.

The following is a set of guidelines for contributing. These are mostly guidelines, not rules. Use your best judgment, and feel free to suggest changes to this document in a pull request.

## Table of Contents <!-- omit in toc -->

- [Development Deployment](#development-deployment)
- [Debug](#debug)
- [Merge Request](#merge-request)
- [Tools](#tools)
  - [uv](#uv)
  - [ruff](#ruff)
  - [gitleaks](#gitleaks)
  - [pre-commit](#pre-commit)
  - [docker](#docker)
  - [trivy](#trivy)
  - [tokei](#tokei)
  - [csv2md](#csv2md)
  - [readme-generator-for-helm](#readme-generator-for-helm)
  - [cProfile](#cprofile)

## Development Deployment

Here are the steps to set up a development environment to run this application.

1. Clone the repository.
2. Let uv initialize the Python virtual environment and install the dependencies:

```bash
make init-dev
```

3. Install the pre-commit hooks:

```bash
pre-commit install --install-hooks
```

4. Fill in the `.env.template` file with your configuration.
5. Rename the file to `.env`.
6. Run the application:

```bash
make run
```

## Debug

Here useful tips to debug the project's code.

Do you want to debug using builtin VSCode debugger?

- Go to the "Run & Debug" tab
- Start a debugging session (using the project's **launch** configuration from the `.code-workspace` file)

Do you want to debug using command line tool pdb?

```bash
make debug
```

> Note: these commands are valid in the situation when you are debugging from the code, but also when you are using the `DEBUG_ENTRYPOINT` environment variable set to "true" (see [entrypoint.sh](docker/entrypoint.sh)).

## Merge Request

Every time you push some code and consequently open a merge request, do not forget to:

- Build an image of the app and scan it using [trivy](#trivy)
- Update the code statistics table in the [README.md](README.md) file using [tokei](#tokei)
- Update the dependency tree in the [README.md](README.md) file using [uv](#uv)
- If needed
  - Update the environment variables table in the [README.md](README.md) file using [csv2md](#csv2md)

## Tools

### uv

Here are useful commands to manage the Python virtual environment and the dependencies using [uv](https://docs.astral.sh/uv/). The source code of this tool is available [here](https://github.com/astral-sh/uv). Do you want to:

Ensures that all project dependencies (listed in `pyproject.toml`) are installed and up-to-date with the lockfile `uv.lock`?

```bash
uv sync
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

Export dependencies and update requirements files...

- as a **user** and for the project?

```bash
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements.txt
```

- as a **developer**?

```bash
uv export --format requirements-txt --group dev --group lint --no-default-groups --no-emit-project --output-file requirements-dev.txt
```

- as a **QA engineer**?

```bash
uv export --format requirements-txt --group test --no-default-groups --no-emit-project --output-file requirements-test.txt
```

### ruff

Here are useful commands to lint and format code using [ruff](https://docs.astral.sh/ruff/). The source code of this tool is available [here](https://github.com/astral-sh/ruff). Do you want to:

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

### gitleaks

Here are useful commands to detect potential secret leaks using [gitleaks](https://gitleaks.io/). The source code of this tool is available [here](https://github.com/gitleaks/gitleaks). Do you want to:

Scan all the commits

```bash
gitleaks git --redact --verbose
```

### pre-commit

Here are useful commands to manage the git hooks using [pre-commit](https://pre-commit.com/). The source code of this tool is available [here](https://github.com/pre-commit/pre-commit). Do you want to:

Auto-update pre-commit config to the latest repos' versions?

```bash
pre-commit autoupdate
```

Run all the hooks on all the files in the repository?

```bash
pre-commit run --all-files
```

Run all the hooks on a specific file in the repository?

```bash
pre-commit run --files <path/to/file>
```

Produce hook output independent of success?

```bash
pre-commit run --all-files --verbose
```

Run a specific hook?

```bash
pre-commit run <hook-id> --all-files --verbose
```

Uninstall hooks?

```bash
pre-commit uninstall
```

### docker

Here are useful commands to manage the Docker configuration. Do you want to:

- Test the `dockerignore` file?

```bash
rsync --archive --dry-run --exclude-from .dockerignore --verbose . /dev/shm
```

### trivy

Here are useful commands to scan an image using [trivy](https://trivy.dev/latest/). The source code of this tool is available [here](https://github.com/aquasecurity/trivy). Do you want to:

Find vulnerabilities, misconfigurations, secrets in an image?

```bash
trivy image --image-config-scanners misconfig,secret --scanners vuln,secret <app>:latest
```

### tokei

Here are useful commands to generate some code statistics and add them to the README using [tokei](https://github.com/XAMPPRocky/tokei).

- Once installed with your method of choice, run the following command at the root of the repository:

```bash
tokei .
```

- Copy the table from stdout to `README.md` in a code block

### csv2md

Here are useful commands to manage the README documentation using [csv2md](https://pypi.org/project/csv2md/). Do you want to:

Easily update the Markdown table of environment variables?

- Update the file `docs/env.csv`
- Generate the corresponding Markdown table:

```bash
python -m csv2md docs/env.csv
```

- Copy the table from stdout to `README.md`

### readme-generator-for-helm

Here are useful commands to manage the Helm chart documentation using [readme-generator-for-helm](https://github.com/bitnami/readme-generator-for-helm). Do you want to:

Update the README.md in the *helm_chart* directory?

```bash
readme-generator --values helm_chart/values.yaml --readme helm_chart/README.md
```

> Note: For any documentation related contribution, please use a spell checking tool like [Grammarly](https://www.grammarly.com) to avoid typographical and any other type of errors.

### cProfile

Here are useful commands to analyze the code performance and identify bottlenecks using [cProfile](https://docs.python.org/3/library/profile.html).

- Set the environment variable **PROFILING** to "true" to enable this functionality.
- Once you run the application, it should generate a report named "{date}_{app_name}.prof" to the output path by the time it finishes
- Open the report with a text editor or visualize it using [snakeviz](https://jiffyclub.github.io/snakeviz/):

```bash
snakeviz {date}_{app_name}.prof
```
