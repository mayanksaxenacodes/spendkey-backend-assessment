#!/usr/bin/env bash
# -*- coding: utf-8 -*-
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT=$(dirname "${SCRIPTS_DIR}")

error() {
    echo -e "\033[31m$*\033[0m" 1>&2
}

# Use local virtualenv if found
if [ -f "${PROJECT_ROOT}/venv/bin/activate" ]; then
    # shellcheck disable=SC1090
    source "${PROJECT_ROOT}/venv/bin/activate"
fi

command -v ruff >/dev/null || {
    error "ruff not found"
    exit 1
}

set -ex
ruff format --check "$@"
