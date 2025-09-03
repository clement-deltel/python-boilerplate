# Python Boilerplate <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Goal](#goal)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Additional steps](#additional-steps)

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
   - Install & run pre-commit hooks

4. Once done, run the commands below:

```bash
cd ../app-name
code app-name.code-workspace
```

## Additional steps

1. [Makefile](./Makefile)
   - update the *(build|pull|push)-image* tasks based on your application's requirements
   - update the *(create|run)-container* tasks based on your application's requirements
2. [pyproject.toml](./pyproject.toml)
   - `project.classifiers`: review based on the official list of [classifiers](https://pypi.org/classifiers)
   - `tool.ty.environment.python-platform`: switch to Windows if needed
   - `tool.uv.environments`: switch to Windows if needed
   - `tool.uv.required-environments`: switch to Windows if needed
