.PHONY: test help
.DEFAULT_GOAL := help

SHELL := /bin/bash

ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

export ROOTDIR:=$(shell pwd)
export CURRENT_VERSION:=$(shell cat ${ROOTDIR}/streamdeck_manager/_meta.py  | sed -En "s/^__version__\s*=\s*[ubrf]*['\"]([^'\"]+)['\"].*$$/\1/p")
export CURRENT_USER:=$(shell id -u ${USER}):$(shell id -g ${USER})

help:
	@echo -e "You can run tasks with:\n\n$$ make \033[36m<task name>\033[0m\n\nwhere \033[36m<task name>\033[0m is one of the following:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# Environment

env-create: ## (re)create a development environment using tox
	tox -e streamdeck_manager --recreate
	@echo -e "\r\nYou can activate the environment with:\r\n\r\n$$ source ./.tox/streamdeck_manager/bin/activate\r\n"

env-compile: ## compile requirements.txt / requirements-dev.txt using pip-tools
	@pip-compile --no-emit-index-url --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	@pip-compile --no-emit-index-url --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

# Development

install: ## install the package
	pip install --no-cache-dir $(PIP_ARGS) .

uninstall: ## uninstall the package
	pip uninstall -y $(PIP_ARGS) streamdeck_manager || true

develop: uninstall ## install the package in development mode
	pip install --editable $(PIP_ARGS) .

fmt: ## format code using the PEP8 convention
	black streamdeck_manager

lint: ## static code analysis with pylint
	pylint --rcfile streamdeck_manager/.pylintrc -j 0 streamdeck_manager

lint-tests: ## static test code analysis with pylint
	pylint --rcfile tests/.pylintrc tests

code-style: ## check code style against PEP8 conventions
	pycodestyle streamdeck_manager

code-maintainability: ## calculates a maintainability index using radon
	radon mi -s streamdeck_manager

code-locs: ## display metrics (LOCs, number of comments, etc.)
	radon raw --summary streamdeck_manager

code-complexity: ## check cyclomatic complexity using radon
	xenon --max-absolute B --max-modules A --max-average A streamdeck_manager

code-metrics: ## check cyclomatic complexity and print LOCs and maintainability index
	@echo -e "Code complexity:\n" && $(MAKE) code-complexity && \
	echo -e "\nMaintainability:\n" && $(MAKE) code-maintainability && \
	echo -e "\nMetrics:\n" && $(MAKE) code-locs

test: ## run tests with pytest and calculate coverage
	py.test

security: ## check source code for vulnerabilities
	@[ "${REPORT_FORMAT}" ] && ( mkdir -p docs/_build/security && bandit -v -r -f ${REPORT_FORMAT} -o docs/_build/security/index.html streamdeck_manager &> /dev/null ) || true
	bandit -v -r streamdeck_manager

check-dependencies: ## check dependencies for vulnerabilities using safety
	safety check --full-report

# Package & Publish

version: ## get the current package version
	@echo $(CURRENT_VERSION)

version-bump: ## bump the version on the specified PART
	bump2version --current-version $(CURRENT_VERSION) $(PART)

version-bump-tag: ## bump and tag the version on the specified PART
	bump2version --commit --tag --current-version $(CURRENT_VERSION) $(PART)

version-set: ## set the version to the specified VERSION
	bump2version --current-version $(CURRENT_VERSION) --new-version $(VERSION) minor

version-set-tag: ## set and commit the version to the specified VERSION
	bump2version --commit --tag --current-version $(CURRENT_VERSION) --new-version $(VERSION) minor

dist: clean-build clean-pyc ## build wheel package (compiled)
	python setup.py bdist_wheel --cythonize

dist-dev: clean-build clean-pyc ## build wheel package (source code)
	python setup.py bdist_wheel

sdist: clean-build clean-pyc ## build a source distribution (sdist)
	python setup.py sdist

# Cleanup

clean: clean-build clean-dist clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-all: clean clean-env ## remove everything (artifacts, environments & docker)

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find . ! -path './.tox/*' -name '*.egg-info' -exec rm -fr {} +
	find . ! -path './.tox/*' -name '*.egg' -exec rm -f {} +
	find streamdeck_manager -name '*.c' -exec rm -f {} +

clean-dist: ## remove dist packages
	rm -fr dist/

clean-pyc: ## remove Python file artifacts
	find . ! -path './.tox/*' -name '*.pyc' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*.pyo' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*~' -exec rm -f {} +
	find . ! -path './.tox/*' -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -f .coverage

clean-env: ## remove virtual environments (created by tox)
	rm -fr .tox/
