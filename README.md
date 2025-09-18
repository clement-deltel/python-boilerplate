# Python Boilerplate <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Goal](#goal)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Additional Steps](#additional-steps)
- [Python Version Bump](#python-version-bump)

## Goal

This is a boilerplate designed for Python developments, and it is supposed to ease the start of a project and standardize practices.

## Requirements

Gather the pieces of information below before starting:

- Application name
- Application description (optional, ideally in a couple of sentences)
- Customer name (optional)
- AzureDevOps User ID (optional)
- AzureDevOps User Story ID (optional)
- Remote repository URL (optional)

Ensure you have installed the tools listed below:

- [uv](https://github.com/astral-sh/uv) - extremely fast package and project manager. `Rust`
- Using Homebrew
  - [gitleaks](https://github.com/gitleaks/gitleaks) - tool for detecting secrets like passwords, API keys, and tokens in git repos. `Go`
  - [hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter, validate inline bash. `Haskell`
  - [ls-lint](https://github.com/loeffel-io/ls-lint) - directory and filename linter, bring some structure to the project filesystem. `Go`
  - [tokei](https://github.com/XAMPPRocky/tokei) - count your code, quickly. `Rust`
  - [varlock](https://github.com/dmno-dev/varlock) - .env files built for sharing powered by @env-spec decorator comments. `TypeScript` `JavaScript`

Or run the command below:

```bash
make pre-requisites
```

## Getting Started

1. Clone the repository.
2. Run the script `init.sh` and follow the instructions throughout the different prompts.
3. This script will perform the following steps:

   - Check that `find`, `git`, `sed`, and `uv` are installed and available
   - Get user input on information listed in the [Requirements](#requirements) section
   - Create the target directory and copy the files
   - Perform replacements of application name & description, customer name in all files
   - Rename files and directories based on the same replacement rules
   - Update renovate configuration
   - Create and initialize a virtual environment using uv
   - Initialize a Git repository on the branch `main` and add the remote (if any)
   - Stage the files for the initial commit
   - Install & run pre-commit hooks (using [prek](https://prek.j178.dev))

4. Once done, run the commands below:

```bash
cd ../app-name
code app-name.code-workspace
```

## Additional Steps

1. [Makefile](./Makefile)
   - update the *(build|pull|push)-image* tasks based on your application's requirements
   - update the *(create|run)-container* tasks based on your application's requirements
2. [pyproject.toml](./pyproject.toml)
   - `project.classifiers`: review based on the official list of [classifiers](https://pypi.org/classifiers)
   - Switch to Windows if needed:
     - `tool.pyright.pythonPlatform`
     - `tool.ty.environment.python-platform`
     - `tool.uv.environments`
     - `tool.uv.required-environments`

## Python Version Bump

Python versioning scheme is: **{MAJOR}.{MINOR}.{PATCH}**

1. For a **PATCH** version bump, here are the steps:

   - update the full version (e.g. **3.11.13**) in the files
     - [docker/Dockerfile](./docker/Dockerfile)
     - [docker/alpine.Dockerfile](./docker/alpine.Dockerfile)
     - [docker/wheel.Dockerfile](./docker/wheel.Dockerfile)
     - [Makefile](./Makefile)
   - Run the commands below

```bash
rm -f .python-version || true
rm -rf .venv
uv python install ${PYTHON_TARGET_VERSION}
uv sync --frozen
```

> **Note**: It is also possible to just update the [Makefile](./Makefile) and run `make python-bump-patch`.

2. For a **MINOR** version bump, here are the steps:

   - update the `requires-python` string in the [pyproject.toml](./pyproject.toml)
   - update the full version (e.g. **3.11.13**) in the files
     - [docker/Dockerfile](./docker/Dockerfile)
     - [docker/alpine.Dockerfile](./docker/alpine.Dockerfile)
     - [docker/wheel.Dockerfile](./docker/wheel.Dockerfile)
     - [Makefile](./Makefile)
   - update the shorten version (e.g. **3.11**) in the files
     - [.pre-commit-config.yaml](./.pre-commit-config.yaml)
     - [pyproject.toml](./pyproject.toml)
   - update the shorten version without dot (e.g. **311**) in the files
     - [pyproject.toml](./pyproject.toml)
   - Run the commands below

```bash
rm -f .python-version || true
rm -rf .venv
uv python install ${PYTHON_TARGET_VERSION}
uv sync --frozen
```

> **Note**: It is also possible to just update the `requires-python` string in the [pyproject.toml](./pyproject.toml), the [Makefile](./Makefile), and run `make python-bump-minor`.
