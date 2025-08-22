# Python Boilerplate <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Goal](#goal)
- [Requirements](#requirements)
- [Getting Started](#getting-started)

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
  - [gitleaks](https://github.com/gitleaks/gitleaks)
  - [hadolint](https://github.com/hadolint/hadolint)
  - [ls-lint](https://github.com/loeffel-io/ls-lint)
  - [tokei](https://github.com/XAMPPRocky/tokei)
  - [varlock](https://github.com/dmno-dev/varlock)

Or run the command below:

```bash
make pre-requisites
```

## Getting Started

1. Clone the repository.
2. Run the script `init.sh` and follow the instructions throughout the different prompts.
3. This script will perform the following steps:

   - Check that `find`, `git` and `sed` are installed and available
   - Get user input on information listed in the [Requirements](#requirements) section
   - Create the target directory and copy the files
   - Perform replacements of application name & description, customer name in all files
   - Rename files and directories based on the same replacement rules
   - Update renovate configuration
   - Create and initialize a virtual environment using venv
   - Initialize a Git repository and add the remote (if any)
   - Install pre-commit hooks
   - Stage the files for the initial commit

4. Once done, run the commands below:

```bash
cd ../app-name
code app-name.code-workspace
```
