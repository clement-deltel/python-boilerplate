# Contributing <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Development Environment](#development-environment)
- [Debug](#debug)
  - [debugpy - Visual Studio Code integration](#debugpy---visual-studio-code-integration)
  - [pdb](#pdb)
- [Merge Request](#merge-request)

## Introduction

🎉 First off, thanks for taking the time to contribute! 🎉

Anyone who wishes to contribute to this project - whether documentation, features, bug fixes, code cleanup, testing, or code reviews - is very much encouraged to do so.

The following is a set of guidelines for contributing. These are mostly guidelines, not rules. Use your best judgment, and feel free to suggest changes to this document in a pull request.

## Development Environment

The pre-requisites are:

- [uv](https://github.com/astral-sh/uv) - extremely fast package and project manager. `Rust`
- Using Homebrew
  - [gitleaks](https://github.com/gitleaks/gitleaks) - tool for detecting secrets like passwords, API keys, and tokens in git repos. `Go`
  - [hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter, validate inline bash. `Haskell`
  - [ls-lint](https://github.com/loeffel-io/ls-lint) - directory and filename linter, bring some structure to the project filesystem. `Go`
  - [tokei](https://github.com/XAMPPRocky/tokei) - count your code, quickly. `Rust`
  - [varlock](https://github.com/dmno-dev/varlock) - .env files built for sharing powered by @env-spec decorator comments. `TypeScript` `JavaScript`
- Using NPM
  - [readme-generator-for-helm](https://github.com/bitnami/readme-generator-for-helm) - auto generate READMEs for Helm Charts. `JavaScript`

```bash
make pre-requisites

git clone https://github.com/bitnami/readme-generator-for-helm
npm install ./readme-generator-for-helm
```

Here are the steps to set up a development environment to run this application.

1. Clone the repository.
2. Let uv initialize the Python virtual environment and install the dependencies:

```bash
# uv, and then pre-commit installation
make init-dev
```

3. Fill in the `.env.schema` file with your configuration.
4. Rename the file to `.env`.
5. Run the application:

```bash
make run
```

> **Note**: for virtual environment auto activation when opening the project using pyenv, run `make pyenv-init` and then `make pyenv-activate`.

## Debug

Here are useful tips to debug the project's code.

### debugpy - Visual Studio Code integration

- Go to the **Run & Debug** tab
- Start a debugging session (using the project's **launch** configurations from the `.code-workspace` file)
  - **Source Code**: debug directly the source code of the application
  - **Process**: debug the application from a running process
  - **Docker Container**: debug the application from within a Docker container
  - **Kubernetes Pod**: debug the application from within a Kubernetes Pod

### pdb

Do you want to run pdb on a module?

```bash
make debug-module
```

Do you want to run pdb on a program?

```bash
make debug-program
```

Do you want to run pdb on a program installed in the virtual environment?

```bash
make debug-venv-program
```

Do you want to run pdb in a container?

```bash
make run-container-pdb
```

## Merge Request

Every time you push some code and consequently open a merge request, do not forget to:

- Update the code statistics table in the [README.md](README.md#code-statistics) file using [tokei](tools/TOOLS.md#tokei)
- Update the dependency tree in the [README.md](README.md#dependencies) file using [uv](tools/TOOLS.md#uv)
- Update the environment variables table in the [README.md](README.md#configuration) file using [csv2md](tools/TOOLS.md#csv2md)

> **Note**: There are pre-commit hooks to update those section of the README file automatically.

- Scan the repository using [checkov](tools/TOOLS.md#checkov), and [trivy](tools/TOOLS.md#trivy)

```bash
make checkov
make trivy-repo
```

- Build an image of the app and scan it using [dockle](tools/TOOLS.md#dockle), [grype](tools/TOOLS.md#grype), and [trivy](tools/TOOLS.md#trivy)

```bash
make build-image
make dockle-image-security
make grype-image
make trivy-image
```
