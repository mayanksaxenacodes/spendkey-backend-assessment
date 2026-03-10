##
# Makefile configuration
# See: https://www.gnu.org/software/make/manual/make.html
SHELL = bash

.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: init
init: ## Initialise the application for local development.
	./scripts/init.sh

.PHONY: start
start: ## Run this application in development mode.
	./scripts/start.sh

.PHONY: database
database: ## Run a local Postgres database.
	docker compose up -d

.PHONY: install-hooks
install-hooks: ## Install the pre-commit hooks.
	[[ "${VIRTUAL_ENV}" == "" ]] && {
		echo "Please run 'source venv/bin/activate' and try again!"
		exit 1
	}
	pre-commit install
	pre-commit install --hook-type=commit-msg

.PHONY: run-hooks
run-hooks: ## Run pre-commit hooks.
	[[ "${VIRTUAL_ENV}" == "" ]] && {
		echo "Please run 'source venv/bin/activate' and try again!"
		exit 1
	}
	pre-commit run --all-files --color=never

.PHONY: unit
unit: ## Run the unit test suite.
	./scripts/unit.sh

.PHONY: help
help:  ## Print this help.
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sed 's/Makefile://' | \
		sort -d | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Silence output by default, use `VERBOSE=1 make <command>` to enable.
ifndef VERBOSE
.SILENT:
endif
