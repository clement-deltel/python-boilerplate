#!/bin/bash

if [[ ! -d "requirements" ]]; then
  mkdir -p requirements
fi

uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt --group cve
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt --group cve --group dev --group lint --group typing
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt --group cve --group test

git add requirements/
