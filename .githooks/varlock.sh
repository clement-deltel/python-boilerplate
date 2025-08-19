#!/bin/bash

if command -v varlock &> /dev/null; then
  varlock load
fi
