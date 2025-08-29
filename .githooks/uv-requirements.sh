#!/bin/bash

if [[ ! -d "requirements" ]]; then
  mkdir -p requirements
fi

uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt --group dev --group lint
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt --group test

git add requirements/
