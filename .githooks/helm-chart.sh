#!/bin/bash

DIRECTORY="helm_chart"

if [[ -d "${DIRECTORY}/" ]]; then
  echo "Linting Helm Chart..."
  helm lint ${DIRECTORY}

  if [[ -f "${DIRECTORY}/values.yaml" ]] && command -v readme-generator &> /dev/null; then
    echo "Updating Helm Chart README.md file..."
    readme-generator --values ${DIRECTORY}/values.yaml --readme ${DIRECTORY}/README.md
    git add ${DIRECTORY}/README.md
  fi
fi
