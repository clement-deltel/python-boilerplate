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
      - 1 `customer-app-name` occurrence
      - 16 `app-name` occurrences
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
    - 2 `Application Name` occurrence
    - 2 `app_name` occurrence
    - add launch configurations if needed
  - **checkov.yaml**
    - 1 `app-name` occurrence
  - **CONTRIBUTING.md**
    - 4 `app-name` occurrence
  - **LICENSE**: delete this file
  - **Makefile**
    - 3 `customer_app-name` occurrences
    - 18 `app-name` occurrences
    - 7 `app_name` occurrences
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

### Naming conventions

General:

- avoid using names that are too general or too wordy, strike a good balance between the two
- capitalize all letters of an abbreviation when using camel case names

Packages & Modules:

- use lower case
- use an underscore as a separator when multiple words are needed
- prefer to stick to 1 word names

Classes:

- use the UpperCaseCamelCase convention
- end exception classes in “Error”

### Coding

- avoid .dot operations (`from math import sqrt` instead of `import math` and then `math.sqrt()`)
- import and use pathlib over os
- use joinpath over "/" to concatenate paths
- use "err" over "e" in exception handling
- use ternary operator when possible
- use Google-style docstrings
- use type annotations
- use | over Union[] for type annotations if needed
- do not use f-strings in log statements

Here are the useful tips to make Python faster:

- apply multi-assignments
- avoid using globals
- use join to concatenate strings
- use code maps to optimize loops
- use built-in functions
- use generator expressions instead of list comprehensions
- use generators and keys for sorting
- use list comprehension instead of loop when possible
- use numpy arrays instead of lists
- use concurrency, multiprocessing
- use pypy

Here are the useful tips to make Python code cleaner:

- use a linter
- use a static type checker
- use a formatter

### Docker

- **Image Management**
  - pin an image version
  - use multi-stage builds to reduce image size
  - consolidate multiple RUN instructions
  - clean the apt/dnf/yum package cache
  - combine the package manager update command with the install
  - use `--no-install-recommends` with `apt-get`
- **Clean**
  - exclude unnecessary files with .dockerignore
  - use `apt-get` or `apt-cache` instead of `apt`
  - choose one or the other: `curl` or `wget`
  - use absolute path for WORKDIR
  - use WORKDIR instead of the cd command
  - use JSON notation for CMD and ENTRYPOINT
  - ensure trailing slash for COPY commands with multiple arguments
  - avoid multiple CMD or ENTRYPOINT instructions
  - avoid multiple HEALTHCHECK instructions
- **Security**
  - avoid default, root, or dynamic user
  - avoid exposing the SSH port
  - avoid overriding ARG variables in RUN commands
  - avoid pipe curl to bash
  - avoid storing secrets in ENV keys
  - avoid using RUN with sudo
  - use COPY instead of ADD

## Resources

- [pyOpenSci - Python Package Guide](https://www.pyopensci.org/python-package-guide/index.html)
- [Python Coding Conventions](https://visualgit.readthedocs.io/en/latest/index.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest)
