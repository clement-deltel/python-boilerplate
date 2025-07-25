# Good Practices <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [New Project](#new-project)
- [Libraries](#libraries)
- [Visual Studio Code extensions](#visual-studio-code-extensions)
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
    - **Dockerfile** or **wheel.Dockerfile** based on your needs
      - image.title
      - image.description
      - image.authors
      - image.vendor
    - **entrypoint.sh**
      - 1 `app` occurrence (use hyphen over underscore if multiple words)
  - *src directory*
    - rename the `app` directory (use hyphen over underscore if multiple words)
    - all `app.*` imports in the Python files
  - **app.code-workspace**
    - rename the file replacing `app`
    - add launch configurations if needed
  - **CONTRIBUTING.md**
    - 1 `<app>` occurrence
  - **LICENSE**: delete this file
  - **Makefile**
    - 18 `app` occurrences
    - check *run* and *debug* tasks to ensure they are compatible with your project
    - update the *(build|pull|push)-image* tasks based on your project's requirements
    - update the *(create|run)-container* tasks based on your project's requirements
  - **pyproject.toml**
    - 9 `app` occurrences
    - project.description
    - project.authors
    - project.maintainers
    - project.classifiers ([list of classifiers](https://pypi.org/classifiers))
    - tool.ty.environment.python-platform (switch to Windows if needed)
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
  - [commitizen](https://github.com/commitizen-tools/commitizen) - committing rules for projects, auto bump versions, and changelog generation. `Python`
  - [csv2md](https://github.com/lzakharov/csv2md) - command line tool for converting CSV files into Markdown tables. `Python`
  - [isort](https://github.com/PyCQA/isort) - utility to sort imports. `Python`
  - [mypy](https://github.com/python/mypy) - static typing. `Python`
  - [pre-commit](https://github.com/pre-commit/pre-commit) - framework for managing and maintaining multi-language pre-commit hooks. `Python`
  - [ruff](https://github.com/astral-sh/ruff) - extremely fast  linter and code formatter. `Rust`
  - [snakeviz](https://github.com/jiffyclub/snakeviz) - in-browser  profile viewer. `Python`
  - [ty](https://github.com/astral-sh/ty) - type checker and language server. `Rust`
  - [uv](https://github.com/astral-sh/uv) - extremely fast package and project manager. `Rust`
  - [yapf](https://github.com/google/yapf) - formatter for files. `Python`

Not using anymore:

- [poetry](https://github.com/python-poetry/poetry) - packaging and dependency management made easy. **Reason**: now using uv. `Python`
- [pyenv](https://github.com/pyenv/pyenv) - version management. **Reason**: now using uv.

## Visual Studio Code extensions

- [autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [pre-commit](https://marketplace.visualstudio.com/items?itemName=elagil.pre-commit-helper)
- [python indent](https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent)
- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [ty](https://marketplace.visualstudio.com/items?itemName=astral-sh.ty)

Not using anymore:

- [poetry](https://marketplace.visualstudio.com/items?itemName=zeshuaro.vscode-python-poetry). **Reason**: now using uv.

## Git hooks

Here are the useful git hooks used across all of my Python projects:

- Featured
  - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
  - [gitleaks](https://github.com/gitleaks/gitleaks)
  - [isort](https://github.com/PyCQA/isort)
  - [ruff](https://github.com/astral-sh/ruff-pre-commit)
  - [shellcheck](https://github.com/shellcheck-py/shellcheck-py)
  - [typos](https://github.com/crate-ci/typos)
  - [uv](https://github.com/astral-sh/uv-pre-commit)
  - [yamllint](https://github.com/adrienverge/yamllint)
- Custom
  - [ls-lint](https://github.com/loeffel-io/ls-lint)
  - [pre-validate-user-email](.githooks/pre-validate-user-email.sh)

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
  - [Ruff-specific - RUF](https://docs.astral.sh/ruff/rules/#ruff-specific-rules-ruf)
- use a formatter

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
