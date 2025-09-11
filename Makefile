# Makefile for generating and packaging the Python SDK

# Variables
PYTHON      := python3
ENV_NAME    := .venv
PIP         := $(ENV_NAME)/bin/pip
API_SPEC_REPO := git@github.com:aviaryhq/cloudglue-api-spec.git
API_SPEC_DIR  := spec
API_SPEC_FILE := $(API_SPEC_DIR)/spec/openapi.json
GENERATE_OP := openapi-generator generate \
               -i $(API_SPEC_FILE) \
               -g python \
               -o temp-sdk \
               --additional-properties=packageName=cloudglue.sdk

# Default target when just running `make`
default: help

## help: Show available make targets
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  setup          Create and activate a local virtual environment and install deps"
	@echo "  submodule-init Initialize the API spec Git submodule"
	@echo "  submodule-update Update the API spec Git submodule to latest version"
	@echo "  generate       Generate Python SDK code from the OpenAPI spec into ./cloudglue/sdk"
	@echo "  build          Build the Python package (wheel + sdist)"
	@echo "  publish        Publish package to PyPI using Twine"
	@echo "  clean          Remove build artifacts, generated code, and the virtual env"

## setup: Create virtual environment and install local Python dependencies
setup:
	$(PYTHON) -m venv $(ENV_NAME)
	$(ENV_NAME)/bin/pip install --upgrade pip setuptools wheel twine build
	$(ENV_NAME)/bin/pip install openapi-generator-cli
#  If you have a requirements.txt for development/build dependencies:
#	$(PIP) install -r requirements.txt

## submodule-init: Initialize the API spec Git submodule
submodule-init:
	@echo "Initializing API spec submodule..."
	git submodule add $(API_SPEC_REPO) $(API_SPEC_DIR) || echo "Submodule already exists"
	git submodule update --init --recursive
	@echo "API spec submodule initialized successfully."

## submodule-update: Update the API spec Git submodule to latest version
submodule-update:
	@echo "Updating API spec submodule..."
	git submodule update --remote --merge $(API_SPEC_DIR)
	@echo "API spec submodule updated successfully."

## generate: Use openapi-generator to produce Python client code and move it to the right location
generate:
	@echo "Generating SDK from OpenAPI spec..."
	# Check if the OpenAPI spec exists
	@if [ ! -f "$(API_SPEC_FILE)" ]; then \
		echo "Error: OpenAPI spec not found at $(API_SPEC_FILE)"; \
		echo "Run 'make submodule-init' to initialize the API spec submodule first."; \
		exit 1; \
	fi
	# First generate to a temporary directory
	rm -rf temp-sdk
	$(GENERATE_OP)
	
	# Clear out previous SDK
	rm -rf cloudglue/sdk/*
	
	# Ensure SDK directory exists
	mkdir -p cloudglue/sdk
	
	# Copy all generated files but restructure them correctly
	@echo "Restructuring generated files..."
	cp -r temp-sdk/cloudglue/sdk/* cloudglue/sdk/
	cp temp-sdk/*.md cloudglue/sdk/ 2>/dev/null || true
	
	# Create __init__.py files if needed
	touch cloudglue/sdk/__init__.py
	
	# Post-process generated files to fix oneOf constraints
	@echo "Post-processing generated files to fix oneOf constraints..."
	$(PYTHON) fix-oneof-constraints.py
	
	# Clean up temporary directory
	rm -rf temp-sdk
	
	@echo "SDK generation complete. Files placed in cloudglue/sdk/"

## build: Build sdist and wheel from the package
build:
	$(ENV_NAME)/bin/pip install build
	$(ENV_NAME)/bin/python -m build

## publish: Upload to PyPI (make sure you have credentials in ~/.pypirc)
publish:
	$(ENV_NAME)/bin/twine upload dist/*

## clean: Remove generated artifacts, dist files, and virtual env
clean:
	rm -rf $(ENV_NAME)
	rm -rf cloudglue/sdk
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf cloudglue.egg-info
	find . -name '__pycache__' -exec rm -rf {} \; 2>/dev/null || true
	find . -name '*.pyc' -delete
	find . -name '.DS_Store' -delete
	find . -name '*.so' -delete
	find . -name '*.c' -delete
	find . -name '*.pyc' -delete
	find . -type d -name "__pycache__" -exec rm -rf {} \; 2>/dev/null || true
	# Don't delete empty directories that might be git repositories
	find . -type d -empty -not -path "./$(API_SPEC_DIR)/*" -not -path "./$(API_SPEC_DIR)" -delete 2>/dev/null || true
