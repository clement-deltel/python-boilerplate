#!/bin/bash

if [[ -d "helm_chart" ]]; then
  helm lint helm_chart
fi
