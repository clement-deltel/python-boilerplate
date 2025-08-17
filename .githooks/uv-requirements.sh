#!/bin/bash

if [[ ! -d "requirements" ]]; then
  mkdir -p requirements
fi

uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
uv export --format requirements-txt --group dev --group lint --no-default-groups --no-emit-project --output-file requirements/requirements-dev.txt
uv export --format requirements-txt --group test --no-default-groups --no-emit-project --output-file requirements/requirements-test.txt

git add requirements/
