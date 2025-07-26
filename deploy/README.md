# Deployment Guide <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Helm commands](#helm-commands)
  - [Registry authentication](#registry-authentication)
  - [Template](#template)
  - [Upgrade \& Uninstall](#upgrade--uninstall)
  - [Rollback](#rollback)

## Introduction

This application production deployment is managed using [Helm](https://helm.sh). The Helm Chart help you define, install, and upgrade everything regarding this application. Helm official documentation is available [here](https://helm.sh/docs).

## Requirements

The core requirements are:

- [kubectl](https://github.com/kubernetes/kubectl)  - Kubernetes command-line interface. `Go`
- [helm](https://github.com/helm/helm)  - Kubernetes package manager. `Go`

Some extra utilities are:

- [k9s](https://github.com/derailed/k9s)  - CLI to manage your clusters in style. `Go`
- [helmfile](https://github.com/helmfile/helmfile)  - declaratively deploy your manifests, Kustomize configs, and Charts as Helm releases. `Go`

The application Helm Chart being hosted on <>, you must be registered and have some credentials.

## Helm commands

### Registry authentication

Authenticate against the registry:

```bash
echo ${PASSWORD} | helm registry login --username <username> --password-stdin <registry>>
```

### Template

Examine the generated deployment using a `values.yaml` file with a dry-run:

```sh
helm template <app> --namespace <namespace> --values ./deploy/custom-values.yaml ./helm_chart > template.yaml
```

### Upgrade & Uninstall

Deploy the application in the Kubernetes cluster using the chart stored in the registry:

```sh
helm upgrade <app>  oci://<registry>/<app> --history-max 5 --install --namespace <namespace> --values ./deploy/custom-values.yaml --version <version>
```

Uninstall the application:

```sh
helm uninstall <app> --namespace <namespace>
```

### Rollback

Check revision numbers:

```bash
helm history <app>
```

Rollback to a previous revision:

```bash
helm rollback <app> <revision> --history-max 5 --namespace <namespace> --recreate-pods
```
