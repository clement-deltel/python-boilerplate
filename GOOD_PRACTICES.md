# Good Practices <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [New Project](#new-project)
- [Good practices](#good-practices)
  - [Naming conventions](#naming-conventions)
  - [Coding](#coding)
  - [Docker](#docker)
- [Resources](#resources)

## Introduction

This document lists and describes all the good practices when it comes to code in Python.

## New Project

Here are the steps you need to follow when starting a new coding project from this boilerplate:

- Clone the repository
- Delete the .git directory
- Update the following directories, files and their fields
  - *.githooks directory*
    - **pre-validate-user-email.sh**
      - 2 `company.com` occurrences
  - *deploy directory*
    - **README.md**
      - 1 `customer` occurrence
      - 17 `app-name` occurrences
      - all `<[a-z]*>` occurrences
  - *docker directory*
    - **compose.yaml**
      - 3 `app-name` occurrences
    - **Dockerfile** or **wheel.Dockerfile** based on your needs
      - 1 `app-name` occurrence
      - 1 `app-description` occurrence
      - image.authors
      - image.vendor
    - **entrypoint.sh**
      - 1 `app_name` occurrence
    - **healthcheck.py**
      - 1 `app_name` occurrence (use underscore over hyphen if multiple words)
  - *src directory*
    - rename the `app_name` directory
    - all `app_name.*` imports in the Python files
  - **.pre-commit-config.yaml**
    - enable commitizen hooks (disabled by default due to lack of emojis support)
  - **app-name.code-workspace**
    - rename the file itself replacing `app-name`
    - 1 `Application Name` occurrence
    - 2 `app_name` occurrence
    - add launch configurations if needed
  - **checkov.yaml**
    - 1 `app-name` occurrence
  - **CONTRIBUTING.md**
    - 4 `app-name` occurrence
  - **LICENSE**: delete this file
  - **Makefile**
    - 1 `customer` occurrence
    - 1 `app-name` occurrence
    - 1 `app_name` occurrence
  - **pyproject.toml**
    - 1 `app-name` occurrence
    - 7 `app_name` occurrences
    - 1 `app-description` occurrence
    - project.authors
    - project.maintainers
  - **README_app.md**
    - rename the file itself removing `_app`
    - 5 `app-name` occurrences
    - 1 `app-description` occurrence
    - 1 `Application Name` occurrence
  - **renovate.json**
    - 1 `azureWorkItemId` occurrence
    - 1 `DOMAIN\\azure_user_id` occurrence
- Additional checks
  - **Makefile**
    - update the *(build|pull|push)-image* tasks based on your application's requirements
    - update the *(create|run)-container* tasks based on your application's requirements
  - **pyproject.toml**
    - `project.classifiers`: review based on the official list of [classifiers](https://pypi.org/classifiers)
    - Switch to Windows if needed:
      - `tool.pyright.pythonPlatform`
      - `tool.ty.environment.python-platform`
      - `tool.uv.environments`
      - `tool.uv.required-environments`
- Run the following uv command: `make init-dev`

## Good practices

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

### Naming conventions

- **General**
  - MUST capitalize all letters of an abbreviation when using camel case names
  - SHOULD NOT use names that are too general or too wordy, strike a good balance between the two
- **Packages & Modules**
  - MUST be lower case
  - MUST use an underscore as a separator when multiple words are needed
  - SHOULD prefer to stick to 1 word names
- **Classes**
  - MUST use the UpperCaseCamelCase convention
  - MUST end exception classes in “Error”
- **Methods & Variables**
  - MUST be lower case
  - MUST use an underscore as a separator when multiple words are needed
  - non-public methods/instance variables SHOULD begin with a single underscore
- **Method arguments**
  - instance methods SHOULD have their first argument named `self`
  - class methods SHOULD have their first argument named `cls`
- **Functions**
  - MUST be lower case
  - MUST use an underscore as a separator when multiple words are needed
- **Constants**
  - MUST be upper case
  - MUST use an underscore as a separator when multiple words are needed

### Coding

- **General**
  - MUST use pathlib over os
  - MUST use `joinpath` over `/` to concatenate paths
  - MUST use "err" over "e" in exception handling
  - MUST NOT use f-strings in log statements
  - SHOULD use ternary operator
  - SHOULD NOT use .dot operations (`from math import sqrt` instead of `import math` and then `math.sqrt()`)
- **Documentation**
  - MUST use Google-style docstrings
  - MUST use type annotations
  - MUST use `|` over `Union[]` for type annotations if needed
- **Faster**
  - SHOULD use multi-assignments
  - SHOULD use `join` to concatenate strings
  - SHOULD use code maps to optimize loops
  - SHOULD use built-in functions
  - SHOULD use generator expressions instead of list comprehensions
  - SHOULD use generators and keys for sorting
  - SHOULD use list comprehension instead of loop when possible
  - SHOULD use numpy arrays instead of lists
  - SHOULD NOT use globals when possible
  - MAY use concurrency, multiprocessing
  - MAY use pypy
- **Cleaner**
  - MUST use a linter
  - MUST use a formatter
  - MUST use a static type checker

### Docker

- **Image Management**
  - MUST pin an image version
  - MUST use multi-stage builds to reduce image size
  - MUST combine the package manager update command with the install
  - MUST use `--no-install-recommends` with `apt-get`
  - SHOULD create reusable stages
  - SHOULD consolidate multiple RUN instructions
  - SHOULD clean the apt/dnf/yum package cache
- **Clean**
  - MUST exclude unnecessary files with .dockerignore
  - MUST sort multi-line arguments
  - MUST use `apt-get` or `apt-cache` instead of `apt`
  - MUST choose one or the other: `curl` or `wget`
  - MUST use absolute path for WORKDIR
  - MUST use WORKDIR instead of the cd command
  - MUST NOT use multiple CMD or ENTRYPOINT instructions
  - MUST NOT use multiple HEALTHCHECK instructions
  - SHOULD use JSON notation for CMD and ENTRYPOINT
  - SHOULD ensure trailing slash for COPY commands with multiple arguments
- **Security**
  - MUST use COPY instead of ADD
  - MUST NOT use default, root, or dynamic user
  - MUST NOT expose the SSH port
  - MUST NOT store secrets in ENV keys
  - SHOULD NOT override ARG variables in RUN commands
  - SHOULD NOT pipe curl to bash
  - SHOULD NOT use RUN with sudo

## Resources

- [PEP 8 — the Style Guide for Python Code](https://pep8.org)
- [pyOpenSci - Python Package Guide](https://www.pyopensci.org/python-package-guide/index.html)
- [Python Coding Conventions](https://visualgit.readthedocs.io/en/latest/index.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org)
