# Deployment Guide <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Kubernetes Workloads](#kubernetes-workloads)
  - [CronJob](#cronjob)
- [Kubernetes Configuration](#kubernetes-configuration)
  - [Secrets](#secrets)
    - [Secret from env file](#secret-from-env-file)
    - [Use External Secret Providers](#use-external-secret-providers)
      - [Hashicorp Vault](#hashicorp-vault)
- [Kubernetes Storage](#kubernetes-storage)
  - [Persistent Volumes](#persistent-volumes)
  - [Persistent Volume Claims](#persistent-volume-claims)
- [Helm](#helm)
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

- [k9s](https://github.com/derailed/k9s)  - CLI to manage Kubernetes clusters in style. `Go`
- [helmfile](https://github.com/helmfile/helmfile)  - declaratively deploy manifests, Kustomize configs, and Charts as Helm releases. `Go`

The application Helm Chart being hosted on <>, you must be registered and have some credentials.

## Kubernetes Workloads

### CronJob

[Link to official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs)

The Kubernetes CronJob object is meant for performing regular scheduled actions, like one line of a crontab file on a Unix system.

## Kubernetes Configuration

### Secrets

[Link to official documentation](https://kubernetes.io/docs/concepts/configuration/secret)

#### Secret from env file

This application Helm chart optionally depends on a `appName.existingSecretName` for providing environment variables, including credentials and application context.

- Fill out the secret template located at `./helm_chart/secret_templates/app-name.env` with the production environment variables.
- Create the corresponding Kubernetes manifest:

```bash
kubectl create secret generic app-name \
--dry-run=client \
--from-env-file=./helm_chart/secret_templates/app-name.env \
--namespace=<namespace> \
--output=yaml \
> ./helm_chart/secret_templates/secret_app-name.yaml
```

- Apply the configuration to the secret resource:

```bash
kubectl apply -f ./helm_chart/secret_templates/secret_app-name.yaml
```

- Fill out the secret name into the `deploy/custom-values.yaml` file before deploying with Helm:

```diff
# ./deploy/custom-values.yaml
appName:
+  existingSecretName: app-name
```

#### Use External Secret Providers

##### Hashicorp Vault

[Link to official documentation](https://developer.hashicorp.com/vault/docs)

Instead of storing secrets directly within Kubernetes, with is unencrypted by default, it is possible to use external secret store providers, like Hashicorp Vault. This guide does not cover the configuration and deployment of Vault in a Kubernetes cluster, but rather the way to use it in the context of this application.

- Create the key-value (KV) store if needed:

```bash
vault secrets enable -path=secret kv
```

- Enable and configure the Kubernetes authentication method:

```bash
vault auth enable kubernetes
vault write auth/kubernetes/config kubernetes_host="https://<kubernetes-port-443-tcp-addr>:443"
```

- Create Vault policy (adapt path if needed):

```bash
vault policy write app-name - <<EOF
path "secret/data/app-name" {
  capabilities = ["read"]
}
EOF
```

- Create a Kubernetes authentication role:

```bash
vault write auth/kubernetes/role/app-name \
    bound_service_account_names=app-name-sa \
    bound_service_account_namespaces=<namespace> \
    policies=app-name \
    ttl=20m
```

- Install the secret CSI driver in the Kubernetes cluster using Helm

```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install csi secrets-store-csi-driver/secrets-store-csi-driver --set syncSecret.enabled=true --set enableSecretRotation=true
```

## Kubernetes Storage

### Persistent Volumes

[Link to official documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes)

The Kubernetes PersistentVolume (or PV) object is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes.

### Persistent Volume Claims

[Link to official documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)

The Kubernetes PersistentVolumeClaim (or PVC) object is a request for storage by a user, and allow this user to consume abstract storage resources. PVCs consume PV resources.

## Helm

### Registry authentication

Authenticate against the registry:

```bash
echo ${PASSWORD} | helm registry login --username <username> --password-stdin <registry>
```

### Template

Examine the generated deployment using a `values.yaml` file with a dry-run:

```sh
helm template app-name --namespace <namespace> --values ./deploy/custom-values.yaml ./helm_chart > template.yaml
```

### Upgrade & Uninstall

Deploy the application in the Kubernetes cluster using the chart stored in the registry:

```sh
helm upgrade app-name  oci://<registry>/customer-app-name --history-max 2 --install --namespace <namespace> --values ./deploy/custom-values.yaml --version <version>
```

Uninstall the application:

```sh
helm uninstall app-name --namespace <namespace>
```

### Rollback

Check revision numbers:

```bash
helm history app-name
```

Rollback to a previous revision:

```bash
helm rollback app-name <revision> --history-max 5 --namespace <namespace> --recreate-pods
```
