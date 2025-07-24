# Project <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Code Statistics](#code-statistics)
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
  - [Code](#code)
  - [Docker](#docker)
  - [Docker Compose](#docker-compose)
- [Production Deployment](#production-deployment)
- [Test](#test)
- [Links](#links)
- [Support and feedback](#support-and-feedback)
- [Resources](#resources)

## Introduction

This application...

## Code Statistics

```text
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 Dockerfile              2          119           57           38           24
 INI                     1           14            5            7            2
 JSON                    1            7            7            0            0
 Makefile                1          113           70           21           22
 Python                  4          584          424           50          110
 Shell                   1            8            6            2            0
 Plain Text              3          416            0          416            0
 TOML                    1          257          137           83           37
 YAML                    1           20           20            0            0
-------------------------------------------------------------------------------
 Markdown                4          876            0          604          272
 |- BASH                 2           68           62            6            0
 (Total)                            944           62          610          272
===============================================================================
 Total                  19         2414          726         1221          467
===============================================================================
```

*generated using [tokei](https://github.com/XAMPPRocky/tokei).*

## Requirements

The core requirements are:

- Python: 3.11.8

Some extra utilities are:

- [ls-lint](https://ls-lint.org/) - directory and filename linter, bring some structure to the project filesystem. `Go`
- [uv](https://docs.astral.sh/uv/) - Python package and project manager. `Rust`
- [varlock](https://varlock.dev/) - .env files powered by @env-spec decorator comments. `TypeScript` `JavaScript`

## Dependencies

This project's dependencies are managed with [uv](https://docs.astral.sh/uv/). You can find more information on how to install it on your system [here](https://docs.astral.sh/uv/getting-started/installation/). It is recommended to install and use it, even still requirements files are available and can be used.

```text
app v0.1.0
├── numpy v2.3.1
├── pandas v2.3.1
│   ├── numpy v2.3.1
│   ├── python-dateutil v2.9.0.post0
│   │   └── six v1.17.0
│   ├── pytz v2025.2
│   └── tzdata v2025.2
├── python-dotenv v1.1.1
└── requests v2.32.4
    ├── certifi v2025.7.14
    ├── charset-normalizer v3.4.2
    ├── idna v3.10
    └── urllib3 v2.5.0
```

## Configuration

The application configuration can be loaded as a set of environment variables in the Docker image. A file mounted on /home/app/.env can also override those values for testing purposes.

List of available environment variables:

> *Note*: for production, it is recommended to store all configuration parameters marked as sensitive with a secrets manager service.

## Quick Start

There are four ways to run this application:

### Code

1. Clone the repository.
2. Let uv initialize the Python virtual environment and install the dependencies:

```bash
make init
```

If using pip, you have to manually:

- Create a Python virtual environment.
- Activate the virtual environment.
- Install the project's dependencies:

```bash
pip install -r requirements/requirements.txt
```

3. Fill in the `.env.template` file with your configuration.
4. Rename the file to `.env`.
5. Run the application:

```bash
make run
```

### Docker

1. Clone the repository.
2. Build the Docker image:

```bash
make build-image
```

3. Fill in the `.env.template` file with your configuration.
4. Rename the file to `.env`.
5. Run the application:

- Run a container:

```bash
make run-container
```

- Create and then run a container:

```bash
# Create
make create-container
# Start
docker start <app>
# or (if you need to attach to the application process)
docker start <app> --attach
```

6. Remove container after execution (if `--rm` option was not used):

```bash
docker rm <app>
```

### Docker Compose

1. Clone this repository.
2. Fill in the `.env.template` file with your configuration.
3. Rename the file to `.env`.
4. Run the application:

- Run a container:

```bash
cd docker
docker compose up --abort-on-container-exit
docker compose down -v
```

- Create and then run a container:

```bash
cd docker
docker compose create
docker compose start
docker logs <app>
docker compose down -v
```

> *Note*: specifically with Docker Compose, if any of your environment variables contains a "\$" character, make sure to put the value between double quotes and escape the "$" with a "\\" character.

## Production Deployment

This application is meant to be deployed in a Kubernetes cluster. To learn more on how to deploy this application, please refer to the guides listed below:

- [Deployment using Helm](deploy/README.md)
- [Helm Chart](helm_chart/README.md)

## Test

If you want to test this application using the released Docker image, follow the steps below:

1. Set your AWS credentials into your environment (using your preferred method) to access AWS resources programmatically.
2. Authenticate to the ECR registry:

```bash
```

3. Pull the image:

```bash
make pull-image
```

4. Run a container:

```bash
make run-container
```

Otherwise, for more in-depth testing and a peak at the code, follow the steps below:

1. Clone this repository.
2. Let uv initialize the Python virtual environment and install the dependencies:

```bash
make init-test
```

If using pip, you have to manually:

- Create a Python virtual environment.
- Activate the virtual environment.
- Install the project's dependencies:


```bash
pip install -r requirements/requirements-test.txt
```

3. Run tests:

- Unit tests:

```bash
make test
```

- Full coverage report:

```bash
make coverage
```

## Links

- See [CHANGELOG.md](CHANGELOG.md) for major/breaking updates.
- To **contribute**, please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Support and feedback

Please open an issue if anything is missing or unclear in this documentation.

## Resources

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:

- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
