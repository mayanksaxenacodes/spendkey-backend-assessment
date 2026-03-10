#!/bin/bash
set -o errexit

if [[ "${VIRTUAL_ENV}" == "" ]]; then
    echo "Please run 'source venv/bin/activate' and try again."
    exit 1
fi

# Immediately dump log messages to the stream.
export PYTHONUNBUFFERED=TRUE

coverage run \
    --source app \
    --module pytest \
    -p no:warnings \
    -vv \
    tests/unit
coverage \
    report \
    --show-missing \
    --skip-empty
