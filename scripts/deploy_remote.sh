#!/usr/bin/env bash
set -euo pipefail

DEPLOY_PATH="${1:-}"
DEPLOY_BRANCH="${2:-main}"

if [[ -z "${DEPLOY_PATH}" ]]; then
  echo "DEPLOY_PATH is required"
  exit 1
fi

if [[ ! -d "${DEPLOY_PATH}" ]]; then
  echo "Directory not found: ${DEPLOY_PATH}"
  exit 1
fi

cd "${DEPLOY_PATH}"

if [[ ! -d ".git" ]]; then
  echo "Not a git repository: ${DEPLOY_PATH}"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Repository has local changes; refusing deploy."
  exit 1
fi

echo "Deploying branch ${DEPLOY_BRANCH} in ${DEPLOY_PATH}"

git fetch origin "${DEPLOY_BRANCH}"
git checkout "${DEPLOY_BRANCH}"
git pull --ff-only origin "${DEPLOY_BRANCH}"

docker compose up -d --build --remove-orphans

echo "Deploy completed"
