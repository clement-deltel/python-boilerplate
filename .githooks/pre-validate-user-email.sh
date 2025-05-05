#!/bin/bash

EMAIL_REGEX="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
ALLOWED_DOMAINS=("company.com" "users.noreply.github.com")

# Create domain regex by joining domains with |
DOMAIN_PATTERN=$(IFS=\| ; echo "${ALLOWED_DOMAINS[*]}")
DOMAIN_REGEX=".*@(${DOMAIN_PATTERN})$"

## Get current user email
USER_EMAIL=$(git config user.email)

## Validate email
if [[ ! ${USER_EMAIL} =~ ${EMAIL_REGEX} ]]; then
  echo "[ERROR] Invalid email format: ${USER_EMAIL}"
  exit 1
fi

## Check email format and domain
if [[ ${USER_EMAIL} =~ ${DOMAIN_REGEX} ]]; then
  echo "Valid email"
  exit 0
else
  echo "[ERROR] Invalid email: ${USER_EMAIL} => Please configure an email and retry."
  echo "Steps:"
  echo '   git config user.email "<user>@company.com"'
  echo "   allowed domains:" "${ALLOWED_DOMAINS[@]}"
  echo ""
  exit 1
fi
