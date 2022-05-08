# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

clean: ## Clean repository
	rm -rf build/ dist/ .eggs/

environment: ## Install packages for development environment
	python3 -m pip install --upgrade flake8 build twine

lint: ## Run the linter for the project
	flake8

build: clean ## Build python package from sources
	python -m build --wheel --sdist

install: clean ## Install python package from sources
	pip install .

install-dev: clean ## Install the python package in development mode
	pip install -e .

uninstall-dev: clean ## Uninstall the package installed in development mode
	rm -rf mypkg.egg-info/
	pip uninstall mypkg

release: ## Release the package
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) python -m twine upload --repository-url $(GITLAB_URL)/projects/$(PROJECT_ID)/packages/pypi dist/*
