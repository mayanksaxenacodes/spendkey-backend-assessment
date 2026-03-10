#!/bin/bash
set -o errexit

# Create a Python virtual environment if it doesn't exist.
[ -d venv ] || python3.13 -m venv venv/

# Activate the virtual environment if it's not already active.
[[ "${VIRTUAL_ENV}" == "" ]] && source venv/bin/activate

# Ensure pip is installed and up-to-date.
python3.13 -m ensurepip --upgrade

# Install development dependencies.
pip install wheel
pip install -r dev/requirements.txt

# Install production dependencies.
pip install -r requirements.txt

# Install pre-commit hooks.
pre-commit install --install-hooks
