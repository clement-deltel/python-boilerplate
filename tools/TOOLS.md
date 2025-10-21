# Tools <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Libraries](#libraries)
- [Pre-commit hooks](#pre-commit-hooks)
- [Lint rules](#lint-rules)
- [Visual Studio Code extensions](#visual-studio-code-extensions)
- [Future enhancements](#future-enhancements)
- [Resources](#resources)

## Introduction

This document lists and describes all the tools that I use when it comes to code in Python.

## Libraries

Here are the useful libraries and modules used across all of my Python projects.

Built-in:

- [cProfile](https://docs.python.org/3/library/profile.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [http](https://docs.python.org/3/library/http.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)

Code:

- [cloudevents](https://github.com/cloudevents/sdk-python) - python SDK for CloudEvents. `Python`
- [numpy](https://github.com/numpy/numpy) - fundamental package for scientific computing. `Python`
- [pika](https://pika.readthedocs.io/en/stable/index.html)
- [polars](https://github.com/pola-rs/polars) - DataFrames powered by a multithreaded, vectorized query engine. `Rust`
- [requests](https://requests.readthedocs.io/en/latest/api)

Development:

- [commitizen](https://github.com/commitizen-tools/commitizen) - committing rules for projects, auto bump versions, and changelog generation. `Python`
- [csv2md](https://github.com/lzakharov/csv2md) - command line tool for converting CSV files into Markdown tables. `Python`
- [howdoi](https://github.com/gleitz/howdoi) - instant coding answers via the command line. `Python`
- [prek](https://github.com/j178/prek) - pre-commit re-engineered. `Rust`
- [snakeviz](https://github.com/jiffyclub/snakeviz) - in-browser profile viewer. `Python`

Lint:

- [checkov](https://github.com/bridgecrewio/checkov) - prevent cloud misconfigurations and find vulnerabilities during build-time in infrastructure as code, container images and open source packages. `Python` `HCL`
- [gitlint](https://github.com/jorisroovers/gitlint) - linting for your git commit messages. `Python`
- [isort](https://github.com/PyCQA/isort) - utility to sort imports. `Python`
- [pyright](https://github.com/microsoft/pyright) - static type checker. `Python`
- [pyupgrade](https://github.com/asottile/pyupgrade) - automatically upgrade syntax for newer versions of the language. `Python`
- [refurb](https://github.com/dosisod/refurb) - refurbishing and modernizing Python codebases. `Python`
- [ruff](https://github.com/astral-sh/ruff-pre-commit) - extremely fast linter and code formatter. `Rust`
- [ty](https://github.com/astral-sh/ty) - type checker and language server. `Rust`
- [yamllint](https://github.com/adrienverge/yamllint) - linter for YAML files. `Python`

Observability:

- [opentelemetry-distro](https://github.com/open-telemetry/opentelemetry-python-contrib) - OpenTelemetry instrumentation for Python modules. `Python`

Test:

- [coverage](https://coverage.readthedocs.io/en/latest)
- [pytest](https://docs.pytest.org/en/stable) -  framework to write small, readable tests, and scale to support complex functional testing for applications and libraries. `Python`

Typing:

- [types-requests](https://pypi.org/project/types-requests)

Not using anymore:

- [mypy](https://github.com/python/mypy) - static typing. **Reason**: using pyright and ty. `Python`
- [pandas](https://pandas.pydata.org/docs/reference/index.html) - **Reason**: using polars.
- [pandas-stubs](https://github.com/VirtusLab/pandas-stubs) - **Reason**: using polars.
- [poetry](https://github.com/python-poetry/poetry) - packaging and dependency management made easy. **Reason**: using uv. `Python`
- [pre-commit](https://github.com/pre-commit/pre-commit) - framework for managing and maintaining multi-language pre-commit hooks. **Reason**: using prek. `Python`
- [pyenv](https://github.com/pyenv/pyenv) - version management. **Reason**: using uv.

## Pre-commit hooks

Here are the useful pre-commit hooks used across all of my Python projects.

- Featured
  - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
  - [commitizen](https://github.com/commitizen-tools/commitizen) - committing rules for projects, auto bump versions, and changelog generation. `Python`
  - [commitlint](https://github.com/conventional-changelog/commitlint) - lint commit messages. `TypeScript`
  - [gitleaks](https://github.com/gitleaks/gitleaks) - tool for detecting secrets like passwords, API keys, and tokens in git repos. `Go`
  - [gitlint](https://github.com/jorisroovers/gitlint) - linting for your git commit messages. `Python`
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
- Other
  - [sync-with-uv](https://github.com/tsvikas/sync-with-uv) - sync .pre-commit-config.yaml from uv.lock. `Python`

Here is a list of pre-commit hooks that could be interesting and further enhance the stack.

- [check-jsonschema](https://github.com/python-jsonschema/check-jsonschema) - CLI and set of pre-commit hooks for jsonschema validation with built-in support for GitHub Workflows, Renovate, Azure Pipelines, and more. `Python`

## Lint rules

Here are the useful lint rules applied across all of my Python projects.

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

## Visual Studio Code extensions

Here are the useful Visual Studio Code used across all of my Python projects.

Docker:

- [hadolint](https://marketplace.visualstudio.com/items?itemName=exiasr.hadolint)
- [vscode-containers](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers)

Git:

- [Git Extension Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.git-extension-pack)
- [pre-commit](https://marketplace.visualstudio.com/items?itemName=elagil.pre-commit-helper)

Kubernetes:

- [Google Cloud Code](https://marketplace.visualstudio.com/items?itemName=googlecloudtools.cloudcode)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
- [Kubernetes Templates](https://marketplace.visualstudio.com/items?itemName=lunuan.kubernetes-templates)

Markdown:

- [markdownlint](https://marketplace.visualstudio.com/items?itemName=davidanson.vscode-markdownlint)
- [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)

Python:

- [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Python Docstring Highlighter](https://marketplace.visualstudio.com/items?itemName=rodolphebarbanneau.python-docstring-highlighter)
- [Python Indent](https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [ty](https://marketplace.visualstudio.com/items?itemName=astral-sh.ty)

Syntax:

- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

TOML:

- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)

Visual Studio Code:

- [Tasks Shell Input](https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input)

Not using anymore:

- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker) **Reason**: using pyright and ty.
- [Python Poetry](https://marketplace.visualstudio.com/items?itemName=zeshuaro.vscode-python-poetry) **Reason**: now using uv.

## Future enhancements

Here is a list of tools that could be interesting and further enhance the stack.

Artificial intelligence:

- [chroma](https://github.com/chroma-core/chroma) - AI-native open-source embedding database. `Rust` `Python`
- [gradio](https://github.com/gradio-app/gradio) - build and share delightful machine learning apps. `Python` `Svelte` `TypeScript`
- [llmlingua](https://github.com/microsoft/LLMLingua) - speed up LLMs' inference and enhance LLM's perceive of key information, compress the prompt and KV-Cache, which achieves up to 20x compression with minimal performance loss. `Python`
- [river](https://github.com/online-ml/river) - online machine learning. `Python`

CLI apps:

- [cyclopts](https://github.com/BrianPugh/cyclopts) - intuitive CLI based on python type hints. `Python`
- [typer](https://github.com/fastapi/typer) - library for building CLI applications. `Python`

Data manipulation:

- [duckdb](https://github.com/duckdb/duckdb) - analytical in-process SQL database management system. `C++`
- [fireducks](https://github.com/fireducks-dev/fireducks) - compiler accelerated dataframe library with fully-compatible pandas API. `C/C++`
- [ibis](https://github.com/ibis-project/ibis) -  portable dataframe library. `Python`
- [prefect](https://github.com/PrefectHQ/prefect) - workflow orchestration framework for building resilient data pipelines. `Python`

Data validation:

- [attrs](https://github.com/python-attrs/attrs) - python classes without boilerplate. `Python`
- [cattrs](https://github.com/python-attrs/cattrs) - composable custom class converters for attrs, dataclasses and friends. `Python`
- [msgspec](https://github.com/jcrist/msgspec) - fast serialization and validation library, with builtin support for JSON, MessagePack, YAML, and TOML. `Python` `C`
- [pydantic](https://github.com/pydantic/pydantic) - data validation using type hints. `Python`

Deployment:

- [score](https://github.com/score-spec/spec) - developer-centric and platform-agnostic Workload specification. `Go`

Documentation:

- [mermaid](https://github.com/mermaid-js/mermaid) - generation of diagrams like flowcharts or sequence diagrams from text in a similar manner as markdown. `TypeScript` `JavaScript`
- [mkdocs](https://github.com/mkdocs/mkdocs) - project documentation with Markdown.
- [sphinx](https://www.sphinx-doc.org/en/master) - documentation generator.
- [pdoc](https://github.com/mitmproxy/pdoc) - API documentation for Python projects. `Python`
- [pydoc](https://docs.python.org/3/library/pydoc.html) - documentation generator and online help system.

Logging:

- [logly](https://github.com/muhammad-fiaz/logly/) - simplify and enhance the logging process. `Python` `Rust`

Make Python faster:

- [cython](https://github.com/cython/cython) - most widely used Python to C compiler.
- [pypy](https://github.com/pypy/pypy) - very fast and compliant implementation of the language.

Profiling:

- [line-profiler](https://github.com/pyutils/line_profiler) - line-by-line profiling. `Python`
- [memory-profiler](https://github.com/pythonprofilers/memory_profiler) - monitor memory usage of Python code. `Python`
- [pyinstrument](https://github.com/joerick/pyinstrument) - call stack profiler. `Python` `TypeScript` `Svelte`
- [py-spy](https://github.com/benfred/py-spy) - sampling profiler for Python programs. `Rust`
- [scalene](https://github.com/plasma-umass/scalene) - high-performance, high-precision CPU, GPU, and memory profiler for Python with AI-powered optimization proposals. `Python` `JavaScript`

Run tasks in parallel:

- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - launching parallel tasks.
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) - process-based parallelism.

Security:

- [pyarmor](https://github.com/dashingsoft/pyarmor) - obfuscate python scripts, bind obfuscated scripts to fixed machine or expire obfuscated scripts. `Python`
- [pycify](https://github.com/tusharsadhwani/pycify) - convert your entire Python project from .py files to .pyc files. `Python`

Terminal:

- [rich](https://github.com/Textualize/rich) - rich text and beautiful formatting in the terminal. `Python`
- [textual](https://github.com/Textualize/textual) - build sophisticated user interfaces with a simple API, run your apps in the terminal and a web browser. `Python`

Type checkers:

- [basedmypy](https://github.com/KotlinIsland/basedmypy) - based Python static type checker with baseline, sane default settings and based typing features. `Python`
- [basedpyright](https://github.com/DetachHead/basedpyright) - pyright fork with various type checking improvements, improved vscode support and pylance features built into the language server. `TypeScript`
- [pylyzer](https://github.com/mtshiba/pylyzer) - fast, feature-rich static code analyzer & language server. `Rust`
- [pyrefly](https://github.com/facebook/pyrefly) - fast type checker and IDE. `Rust`
- [zuban](https://github.com/zubanls/zuban) - type checker / language server. `Rust`

Web:

- [reflex](https://github.com/reflex-dev/reflex) -  full-stack web apps in pure Python. `Python`
- [scrapy](https://github.com/scrapy/scrapy) - fast high-level web crawling & scraping framework. `Python`
- [selenium](https://pypi.org/project/selenium)

Other:

- [Algorithms - Python](https://github.com/TheAlgorithms/Python) - all algorithms. `Python`
- [altair](https://github.com/vega/altair) - declarative visualization library. `Python`
- [moto](https://github.com/getmoto/moto) - easily mock out tests based on AWS infrastructure. `Python`
- [pillow](https://github.com/python-pillow/Pillow) - Python imaging library. `Python`
- [streamlit](https://github.com/streamlit/streamlit) - build and share data apps. `Python` `TypeScript`
- [thepipe](https://github.com/emcf/thepipe) - get clean data from tricky documents, powered by vision-language models. `Python`
- [tqdm](https://github.com/tqdm/tqdm) - fast, extensible progress bar. `Python`
- [yapf](https://github.com/google/yapf) - formatter for files. `Python`

## Resources

- [Top 7 Python Profiling Tools for Performance](https://daily.dev/blog/top-7-python-profiling-tools-for-performance)
