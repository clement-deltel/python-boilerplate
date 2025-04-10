# Good Practices <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Libraries](#libraries)
- [Coding practices](#coding-practices)
- [Future enhancements](#future-enhancements)

## Introduction

This document lists and describes all the good practices when it comes to code in Python.

## Libraries

Here are the useful libraries and modules used across all of my Python projects:

- Built-in
  - [cProfile](https://docs.python.org/3/library/profile.html)
- Third-party
  - [commitizen](https://github.com/commitizen/cz-cli): commitizen command line utility.
  - [csv2md](https://github.com/lzakharov/csv2md): command line tool for converting CSV files into Markdown tables.
  - [mypy](https://github.com/python/mypy): static typing for Python.
  - [poetry](https://github.com/python-poetry/poetry): Python packaging and dependency management made easy.
  - [pre-commit](https://github.com/pre-commit/pre-commit): framework for managing and maintaining multi-language pre-commit hooks.
  - [pyenv](https://github.com/pyenv/pyenv): Python version management.
  - [ruff](https://github.com/astral-sh/ruff): extremely fast Python linter and code formatter, written in Rust.
  - [snakeviz](https://github.com/jiffyclub/snakeviz): in-browser Python profile viewer.
  - [yapf](https://github.com/google/yapf): formatter for Python files.

Aa well as the corresponding Visual Studio Code extensions for some of them:

- [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [poetry](https://marketplace.visualstudio.com/items?itemName=zeshuaro.vscode-python-poetry)
- [pre-commit](https://marketplace.visualstudio.com/items?itemName=elagil.pre-commit-helper)
- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## Coding practices

Here is a list of tips to make Python faster:

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

## Future enhancements

Here is a list of tools that could be interesting and further enhance the stack:

- [pillow](https://github.com/python-pillow/Pillow): Python imaging library.
- [pydantic](https://github.com/pydantic/pydantic): data validation using Python type hints.
- [pylyzer](https://github.com/mtshiba/pylyzer): fast, feature-rich static code analyzer & language server for Python.
- [uv](https://github.com/astral-sh/uv): extremely fast Python package and project manager, written in Rust.
- [uv-pre-commit](https://github.com/astral-sh/uv-pre-commit)

And specifically to make Python faster:

- [cython](https://github.com/cython/cython): most widely used Python to C compiler.
- [pypy](https://github.com/pypy/pypy): very fast and compliant implementation of the Python language.

Drop-in replacement for pandas:

- [fireducks](https://github.com/fireducks-dev/fireducks): compiler accelerated dataframe library for Python with fully-compatible pandas API.
- [polars](https://github.com/pola-rs/polars): dataframes powered by a multithreaded, vectorized query engine, written in Rust.
