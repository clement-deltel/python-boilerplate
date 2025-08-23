#!/bin/bash

if [[ ! -d "requirements" ]]; then
  mkdir -p requirements
fi

uv export --format requirements-txt --no-default-groups --no-emit-project --output-file requirements/requirements.txt
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file --group dev --group lint requirements/requirements-dev.txt
uv export --format requirements-txt --no-default-groups --no-emit-project --output-file --group test requirements/requirements-test.txt

git add requirements/
