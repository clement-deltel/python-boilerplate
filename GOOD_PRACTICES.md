# Good Practices <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [New Project](#new-project)
- [Libraries](#libraries)
- [Visual Studio Code extensions](#visual-studio-code-extensions)
- [Git hooks](#git-hooks)
- [Good practices](#good-practices)
  - [Python coding](#python-coding)
  - [Docker](#docker)
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
    - 6 `customer_app-name` occurrences
    - 15 `app-name` occurrences
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
    - `tool.ty.environment.python-platform`: switch to Windows if needed
    - `tool.uv.environments`: switch to Windows if needed
    - `tool.uv.required-environments`: switch to Windows if needed
- Run the following uv command: `make init-dev`

## Libraries

Here are the useful libraries and modules used across all of my Python projects:

- **Built-in**
  - [cProfile](https://docs.python.org/3/library/profile.html)
  - [http](https://docs.python.org/3/library/http.html)
  - [pathlib](https://docs.python.org/3/library/pathlib.html)
- **Third-party**
  - [checkov](https://github.com/bridgecrewio/checkov) - prevent cloud misconfigurations and find vulnerabilities during build-time in infrastructure as code, container images and open source packages. `Python` `HCL`
  - [cloudevents](https://github.com/cloudevents/sdk-python) - python SDK for CloudEvents. `Python`
  - [coverage](https://coverage.readthedocs.io/en/latest)
  - [csv2md](https://github.com/lzakharov/csv2md) - command line tool for converting CSV files into Markdown tables. `Python`
  - [mypy](https://github.com/python/mypy) - static typing. `Python`
  - [pre-commit](https://github.com/pre-commit/pre-commit) - framework for managing and maintaining multi-language pre-commit hooks. `Python`
  - [pandas](https://pandas.pydata.org/docs/reference/index.html#api)
  - [pika](https://pika.readthedocs.io/en/stable/index.html)
  - [pytest](https://docs.pytest.org/en/stable)
  - [requests](https://requests.readthedocs.io/en/latest/api/)
  - [snakeviz](https://github.com/jiffyclub/snakeviz) - in-browser profile viewer. `Python`
  - [ty](https://github.com/astral-sh/ty) - type checker and language server. `Rust`
  - [yapf](https://github.com/google/yapf) - formatter for files. `Python`

Not using anymore:

- [poetry](https://github.com/python-poetry/poetry) - packaging and dependency management made easy. **Reason**: now using uv. `Python`
- [pyenv](https://github.com/pyenv/pyenv) - version management. **Reason**: now using uv.

## Visual Studio Code extensions

- [autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [hadolint](https://marketplace.visualstudio.com/items?itemName=exiasr.hadolint)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [pre-commit](https://marketplace.visualstudio.com/items?itemName=elagil.pre-commit-helper)
- [python-docstring-highlighter](https://marketplace.visualstudio.com/items?itemName=rodolphebarbanneau.python-docstring-highlighter)
- [python indent](https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent)
- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [ty](https://marketplace.visualstudio.com/items?itemName=astral-sh.ty)

Not using anymore:

- [poetry](https://marketplace.visualstudio.com/items?itemName=zeshuaro.vscode-python-poetry). **Reason**: now using uv.

## Git hooks

Here are the useful git hooks used across all of my Python projects:

- Featured
  - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
  - [commitizen](https://github.com/commitizen-tools/commitizen) - committing rules for projects, auto bump versions, and changelog generation. `Python`
  - [gitleaks](https://github.com/gitleaks/gitleaks) - tool for detecting secrets like passwords, API keys, and tokens in git repos. `Go`
  - [hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter, validate inline bash. `Haskell`
  - [isort](https://github.com/PyCQA/isort) - utility to sort imports. `Python`
  - [pyupgrade](https://github.com/asottile/pyupgrade)
  - [refurb](https://github.com/dosisod/refurb)
  - [ruff](https://github.com/astral-sh/ruff-pre-commit) - extremely fast linter and code formatter. `Rust`
  - [shellcheck](https://github.com/shellcheck-py/shellcheck-py)
  - [typos](https://github.com/crate-ci/typos)
  - [uv](https://github.com/astral-sh/uv-pre-commit) - extremely fast package and project manager. `Rust`
  - [yamllint](https://github.com/adrienverge/yamllint)
- Custom
  - [helm-lint](https://helm.sh/docs/helm/helm_lint)
  - [ls-lint](https://github.com/loeffel-io/ls-lint) - directory and filename linter, bring some structure to the project filesystem. `Go`
  - [pre-validate-user-email](.githooks/pre-validate-user-email.sh)
  - [readme-generator-for-helm](https://github.com/bitnami/readme-generator-for-helm)
  - [readme-update](.githooks/readme_update.py)
  - [varlock](https://github.com/dmno-dev/varlock) - .env files built for sharing powered by @env-spec decorator comments. `TypeScript` `JavaScript`

## Good practices

### Python coding

Here are the essential good practices:

- avoid .dot operations (`from math import sqrt` instead of `import math` and then `math.sqrt()`)
- use pathlib over os module
- use "err" over "e" in exception handling
- use ternary operator when possible
- use Google-style docstrings
- use | for type annotations if needed
- do not use f-strings in log statements

Here are the useful tips to make Python faster:

- apply multi-assignments
- avoid using globals
- concatenate strings with join
- optimize loops with code maps
- use built-in functions
- use generator expressions instead of list comprehensions
- use generators and keys for sorting
- use list comprehension instead of loop when possible
- use numpy arrays instead of lists
- use concurrency, multiprocessing
- use pypy

Here are the useful tips to make Python code cleaner:

- use a linter. As of now, ruff is the default and select the following rules:
  - [eradicate - ERA](https://docs.astral.sh/ruff/rules/#eradicate-era)
  - **flake8**
    - [bandit - S](https://docs.astral.sh/ruff/rules/#flake8-bandit-s)
    - [bugbear - B](https://docs.astral.sh/ruff/rules/#flake8-bugbear-b)
    - [builtins - A](https://docs.astral.sh/ruff/rules/#flake8-builtins-a)
    - [commas - COM](https://docs.astral.sh/ruff/rules/#flake8-commas-com)
    - [comprehensions - C4](https://docs.astral.sh/ruff/rules/#flake8-comprehensions-c4)
    - [datetimez - DTZ](https://docs.astral.sh/ruff/rules/#flake8-datetimez-dtz)
    - [implicit-str-concat - ISC](https://docs.astral.sh/ruff/rules/#flake8-implicit-str-concat-isc)
    - [import-conventions - ICN](https://docs.astral.sh/ruff/rules/#flake8-import-conventions-icn)
    - [logging-format - G](https://docs.astral.sh/ruff/rules/#flake8-logging-format-g)
    - [quotes - Q](https://docs.astral.sh/ruff/rules/#flake8-quotes-q)
    - [raise - RSE](https://docs.astral.sh/ruff/rules/#flake8-raise-rse)
    - [return - RET](https://docs.astral.sh/ruff/rules/#flake8-return-ret)
    - [self - SLF](https://docs.astral.sh/ruff/rules/#flake8-self-slf)
    - [simplify - SIM](https://docs.astral.sh/ruff/rules/#flake8-simplify-sim)
    - [tidy-imports - TID](https://docs.astral.sh/ruff/rules/#flake8-tidy-imports-tid)
    - [unused arguments - ARG](https://docs.astral.sh/ruff/rules/#flake8-unused-arguments-arg)
    - [use-pathlib - PTH](https://docs.astral.sh/ruff/rules/#flake8-use-pathlib-pth)
  - [isort - I](https://docs.astral.sh/ruff/rules/#isort-i)
  - [pandas-vet - PD](https://docs.astral.sh/ruff/rules/#pandas-vet-pd)
  - [pep8-naming - N](https://docs.astral.sh/ruff/rules/#pep8-naming-n)
  - [perflint - PERF](https://docs.astral.sh/ruff/rules/#perflint-perf)
  - [pycodestyle - Errors - E](https://docs.astral.sh/ruff/rules/#pycodestyle-e)
  - [pydocstyle - D](https://docs.astral.sh/ruff/rules/#pydocstyle-d)
  - [Pyflakes - F](https://docs.astral.sh/ruff/rules/#pyflakes-f)
  - [Pylint - PL](https://docs.astral.sh/ruff/rules/#pylint-pl)
  - [pyupgrade - UP](https://docs.astral.sh/ruff/rules/#pyupgrade-up)
  - [refurb - FURB](https://docs.astral.sh/ruff/rules/#refurb-furb)
  - [Ruff-specific - RUF](https://docs.astral.sh/ruff/rules/#ruff-specific-rules-ruf)
- use a formatter

### Docker

Here are the essential good practices:

- **Image Management**
  - Pin an image version
  - Use multi-stage builds to reduce image size
  - Consolidate multiple RUN instructions
  - Clean the apt/dnf/yum package cache
  - Combine the package manager update command with the install
  - Une `--no-install-recommends` with `apt-get`
- **Clean**
  - Exclude unnecessary files with .dockerignore
  - Use `apt-get` or `apt-cache` instead of `apt`
  - Choose one or the other: `curl` or `wget`
  - Use absolute path for WORKDIR
  - Use WORKDIR instead of the cd command
  - Use JSON notation for CMD and ENTRYPOINT
  - Ensure trailing slash for COPY commands with multiple arguments
  - Avoid multiple CMD or ENTRYPOINT instructions
  - Avoid multiple HEALTHCHECK instructions
- **Security**
  - Avoid default, root, or dynamic user
  - Avoid exposing the SSH port
  - Avoid overriding ARG variables in RUN commands
  - Avoid pipe curl to bash
  - Avoid storing secrets in ENV keys
  - Avid using RUN with sudo
  - Use COPY instead of ADD


## Future enhancements

Here is a list of tools that could be interesting and further enhance the stack:

- [altair](https://github.com/vega/altair) - declarative visualization library. `Python`
- [basedmypy](https://github.com/KotlinIsland/basedmypy) - based Python static type checker with baseline, sane default settings and based typing features. `Python`
- [basedpyright](https://github.com/DetachHead/basedpyright) - pyright fork with various type checking improvements, improved vscode support and pylance features built into the language server. `TypeScript`
- [chroma](https://github.com/chroma-core/chroma) - AI-native open-source embedding database. `Rust` `Python`
- [cyclopts](https://github.com/BrianPugh/cyclopts) - intuitive CLI based on python type hints. `Python`
- [duckdb](https://github.com/duckdb/duckdb) - analytical in-process SQL database management system. `C++`
- [ibis](https://github.com/ibis-project/ibis) -  portable dataframe library. `Python`
- [llmlingua](https://github.com/microsoft/LLMLingua) - speed up LLMs' inference and enhance LLM's perceive of key information, compress the prompt and KV-Cache, which achieves up to 20x compression with minimal performance loss. `Python`
- [moto](https://github.com/getmoto/moto) - easily mock out tests based on AWS infrastructure. `Python`
- [pillow](https://github.com/python-pillow/Pillow) - Python imaging library. `Python`
- [pylyzer](https://github.com/mtshiba/pylyzer) - fast, feature-rich static code analyzer & language server. `Rust`
- [pyrefly](https://github.com/facebook/pyrefly) - fast type checker and IDE. `Rust`
- [pyright](https://github.com/microsoft/pyright) - static type checker. `Python`
- [rich](https://github.com/Textualize/rich) - rich text and beautiful formatting in the terminal. `Python`
- [streamlit](https://github.com/streamlit/streamlit) - build and share data apps. `Python` `TypeScript`
- [thepipe](https://github.com/emcf/thepipe) - get clean data from tricky documents, powered by vision-language models. `Python`
- [tqdm](https://github.com/tqdm/tqdm) - fast, extensible progress bar. `Python`
- [typer](https://github.com/fastapi/typer) - library for building CLI applications. `Python`

And specifically to make Python faster:

- [cython](https://github.com/cython/cython) - most widely used Python to C compiler.
- [pypy](https://github.com/pypy/pypy) - very fast and compliant implementation of the language.

And specifically to run tasks in parallel:

- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - launching parallel tasks.
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) - process-based parallelism.

And specifically for data validation:

- [attrs](https://github.com/python-attrs/attrs) - python classes without boilerplate. `Python`
- [cattrs](https://github.com/python-attrs/cattrs) - composable custom class converters for attrs, dataclasses and friends. `Python`
- [msgspec](https://github.com/jcrist/msgspec) - fast serialization and validation library, with builtin support for JSON, MessagePack, YAML, and TOML. `Python` `C`
- [pydantic](https://github.com/pydantic/pydantic) - data validation using type hints. `Python`

And specifically to document the code:

- [mkdocs](https://github.com/mkdocs/mkdocs) - project documentation with Markdown.
- [sphinx](https://www.sphinx-doc.org/en/master) - documentation generator.
- [pydoc](https://docs.python.org/3/library/pydoc.html) - documentation generator and online help system.

Drop-in replacement for pandas:

- [fireducks](https://github.com/fireducks-dev/fireducks) - compiler accelerated dataframe library with fully-compatible pandas API. `C/C++`
- [polars](https://github.com/pola-rs/polars) - DataFrames powered by a multithreaded, vectorized query engine. `Rust`

## Resources

- [pyOpenSci - Python Package Guide](https://www.pyopensci.org/python-package-guide/index.html)
