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
 INI                     1           14            5            7            2
 Makefile                1           32           23            0            9
 Shell                   1            8            6            2            0
 TOML                    1          134           71           46           17
 YAML                    1           20           20            0            0
-------------------------------------------------------------------------------
 Markdown                3          593            0          386          207
 |- BASH                 2           56           53            3            0
 (Total)                            649           53          389          207
===============================================================================
 Total                   8          801          125          441          235
===============================================================================
```

*generated using [tokei](https://github.com/XAMPPRocky/tokei).*

## Requirements

The core requirements are:

- Python: 3.11.8

Some extra utilities are:

- [uv](https://docs.astral.sh/uv/): Python package and project manager.

## Dependencies

This project's dependencies are managed with [uv](https://docs.astral.sh/uv/). You can find more information on how to install it on your system [here](https://docs.astral.sh/uv/getting-started/installation/). It is recommended to install and use it, even still requirements files are available and can be used.

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
uv sync --no-default-groups
```

If using pip, you have to manually:

- Create a Python virtual environment.
- Activate the virtual environment.
- Install the project's dependencies:

```bash
pip install -r requirements.txt
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
make build-container
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
make pull-container
```

4. Run a container:

```bash
make run-container
```

Otherwise, for more in-depth testing and a peak at the code, follow the steps below:

1. Clone this repository.
2. Let uv initialize the Python virtual environment and install the dependencies:

```bash
uv sync --group test --no-default-groups
```

If using pip, you have to manually:

- Create a Python virtual environment.
- Activate the virtual environment.
- Install the project's dependencies:


```bash
pip install -r requirements-test.txt
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
