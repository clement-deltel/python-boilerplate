# Good Practices <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [New Project](#new-project)
- [Libraries](#libraries)
- [Git hooks](#git-hooks)
- [Coding practices](#coding-practices)
- [Future enhancements](#future-enhancements)
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
  - *docker directory*
    - **compose.yaml**
      - container_name
      - hostname
      - image
    - **Dockerfile**
      - image.title
      - image.description
      - image.authors
      - image.vendor
    - **entrypoint.sh**
      - 1 `app` occurrence
  - *src directory*
    - rename the `app` directory
    - all `src.app.*` imports in the Python files
  - **LICENSE**: delete this file
  - **Makefile**
    - 8 `app` occurrences
    - check *run* and *debug* tasks to ensure they are compatible with your project
    - update the *(build|create|pull|run)-container* tasks based on your project's requirements
  - **pyproject.toml**
    - tool.hatch.build.targets.wheel.packages
    - project.name
    - project.description
    - project.authors
    - project.maintainers
    - project.classifiers (full list of possibilities available [here](https://pypi.org/classifiers))
    - tool.uv.environments (switch to Windows if needed)
    - tool.uv.required-environments (switch to Windows if needed)
  - **README.md**
    - 4 `<app>` occurrences
    - Introduction section
- Run the following uv command: `make init-dev`

## Libraries

Here are the useful libraries and modules used across all of my Python projects:

- Built-in
  - [cProfile](https://docs.python.org/3/library/profile.html)
- Third-party
  - [commitizen](https://github.com/commitizen/cz-cli): commitizen command line utility.
  - [csv2md](https://github.com/lzakharov/csv2md): command line tool for converting CSV files into Markdown tables.
  - [mypy](https://github.com/python/mypy): static typing for Python.
  - [pre-commit](https://github.com/pre-commit/pre-commit): framework for managing and maintaining multi-language pre-commit hooks.
  - [ruff](https://github.com/astral-sh/ruff): extremely fast Python linter and code formatter, written in Rust.
  - [snakeviz](https://github.com/jiffyclub/snakeviz): in-browser Python profile viewer.
  - [uv](https://github.com/astral-sh/uv): extremely fast Python package and project manager, written in Rust.
  - [yapf](https://github.com/google/yapf): formatter for Python files.

Not using anymore:

- [poetry](https://github.com/python-poetry/poetry): Python packaging and dependency management made easy.
- [pyenv](https://github.com/pyenv/pyenv): Python version management.

Aa well as the corresponding Visual Studio Code extensions for some of them:

- [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [pre-commit](https://marketplace.visualstudio.com/items?itemName=elagil.pre-commit-helper)
- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

Not using anymore:

- [poetry](https://marketplace.visualstudio.com/items?itemName=zeshuaro.vscode-python-poetry)

## Git hooks

Here are the useful git hooks used across all of my Python projects:

- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [ruff](https://github.com/astral-sh/ruff-pre-commit)
- [shellcheck](https://github.com/shellcheck-py/shellcheck-py)
- [typos](https://github.com/crate-ci/typos)
- [uv](https://github.com/astral-sh/uv-pre-commit)
- [yamllint](https://github.com/adrienverge/yamllint)

## Coding practices

Here are the useful tips to make Python faster:

- apply multi-assignments
- avoid .dot operations (`from math import sqrt` instead of `import math` and then `math.sqrt()`)
- avoid using globals
- concatenate strings with join
- optimize loops with code maps
- use built-in functions
- use concurrency, multiprocessing
- use generator expressions instead of list comprehensions
- use generators and keys for sorting
- use list comprehension instead of loop
- use numpy arrays instead of lists
- use pypy
- use 1 instead of "True" for infinite loops

Here are the useful tips to make Python code cleaner:

- use a linter. As of now, ruff is the default and select the following rules:
  - flake8
    - [bugbear - B](https://docs.astral.sh/ruff/rules/#flake8-bugbear-b)
    - [comprehensions - C4](https://docs.astral.sh/ruff/rules/#flake8-comprehensions-c4)
    - [logging-format - G](https://docs.astral.sh/ruff/rules/#flake8-logging-format-g)
    - [quotes - Q](https://docs.astral.sh/ruff/rules/#flake8-quotes-q)
    - [raise - RSE](https://docs.astral.sh/ruff/rules/#flake8-raise-rse)
    - [return - RET](https://docs.astral.sh/ruff/rules/#flake8-return-ret)
    - [self - SLF](https://docs.astral.sh/ruff/rules/#flake8-self-slf)
    - [simplify - SIM](https://docs.astral.sh/ruff/rules/#flake8-simplify-sim)
    - [use-pathlib - PTH](https://docs.astral.sh/ruff/rules/#flake8-use-pathlib-pth)
  - [isort - I](https://docs.astral.sh/ruff/rules/#isort-i)
  - [pandas-vet - PD](https://docs.astral.sh/ruff/rules/#pandas-vet-pd)
  - [pep8-naming - N](https://docs.astral.sh/ruff/rules/#pep8-naming-n)
  - [pycodestyle - Errors - E](https://docs.astral.sh/ruff/rules/#pycodestyle-e)
  - [pydocstyle - D](https://docs.astral.sh/ruff/rules/#pydocstyle-d)
  - [Pyflakes - F](https://docs.astral.sh/ruff/rules/#pyflakes-f)
  - [Pylint - PL](https://docs.astral.sh/ruff/rules/#pylint-pl)
- use a formatter

## Future enhancements

Here is a list of tools that could be interesting and further enhance the stack:

- [basedmypy](https://github.com/KotlinIsland/basedmypy): based Python static type checker with baseline, sane default settings and based typing features.
- [basedpyright](https://github.com/DetachHead/basedpyright): pyright fork with various type checking improvements, improved vscode support and pylance features built into the language server.
- [pillow](https://github.com/python-pillow/Pillow): Python imaging library.
- [pydantic](https://github.com/pydantic/pydantic): data validation using Python type hints.
- [pylyzer](https://github.com/mtshiba/pylyzer): fast, feature-rich static code analyzer & language server for Python.
- [pyright](https://github.com/microsoft/pyright): static type checker for Python.

And specifically to make Python faster:

- [cython](https://github.com/cython/cython): most widely used Python to C compiler.
- [pypy](https://github.com/pypy/pypy): very fast and compliant implementation of the Python language.

Drop-in replacement for pandas:

- [fireducks](https://github.com/fireducks-dev/fireducks): compiler accelerated dataframe library for Python with fully-compatible pandas API.
- [polars](https://github.com/pola-rs/polars): dataframes powered by a multithreaded, vectorized query engine, written in Rust.

## Resources

- [pyOpenSci - Python Package Guide](https://www.pyopensci.org/python-package-guide/index.html)
