#!/bin/bash
set -o errexit

if [[ "${VIRTUAL_ENV}" == "" ]]; then
    echo "Please run 'source venv/bin/activate' and try again."
    exit 1
fi

export PYTHONUNBUFFERED=TRUE
export CORS_ORIGINS="http://localhost:3000"
export DATABASE_URI="postgresql://postgres:postgres@localhost:5432/spendkey"
export ENABLE_OPENAPI_DOCS="true"

UVICORN_PORT="${PORT:-3000}"

echo "Starting development server on ${UVICORN_PORT}"
uvicorn \
    --factory app.server.factory:create_app \
    --port "${UVICORN_PORT}" \
    --reload
