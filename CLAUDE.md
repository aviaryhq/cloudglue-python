# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

CloudGlue Python SDK - Official SDK for the CloudGlue API that turns video into LLM-ready data. Python 3.10+.

## Common Commands

```bash
make setup              # Create venv and install dependencies
make submodule-init     # Initialize API spec Git submodule (required first time)
make submodule-update   # Update API spec to latest version
make generate           # Regenerate SDK from OpenAPI spec
make build              # Build wheel + sdist
make publish            # Upload to PyPI
make clean              # Remove all build artifacts
```

Install in development mode:
```bash
source .venv/bin/activate
pip install -e .
```

Prerequisite: `brew install openapi-generator`

## Architecture

### Two-Layer Design

1. **Custom Client Layer** (`cloudglue/client/`) - User-friendly interface you edit
   - `main.py` - `CloudGlue` main class, initializes all resources
   - `resources/` - 15 resource wrappers (Chat, Files, Collections, etc.)
   - `resources/base.py` - `CloudGlueError` exception class

2. **Generated SDK Layer** (`cloudglue/sdk/`) - Auto-generated, DO NOT EDIT
   - Generated from OpenAPI spec via `make generate`
   - `api/` - API endpoint classes
   - `models/` - Pydantic models

### Key Patterns

**Resource wrappers** convert `ApiException` to `CloudGlueError`:
```python
try:
    return self.api.some_method(...)
except ApiException as e:
    raise CloudGlueError(str(e), e.status, e.data, e.headers, e.reason)
```

**Filter helpers** use static methods to convert dicts to Pydantic filter objects (see `chat.py` for example).

**Configuration**: API key via constructor or `CLOUDGLUE_API_KEY` env var.

### API Spec

The OpenAPI spec is a Git submodule in `spec/` pointing to `cloudglue-api-spec` repo. After updating the submodule, run `make generate` to regenerate the SDK. The `fix-oneof-constraints.py` script runs post-generation to fix oneOf validation issues.

## Adding a New Resource

1. Ensure the API spec includes the new endpoints
2. Run `make generate` to create API classes and models
3. Create a new resource wrapper in `cloudglue/client/resources/`
4. Import the API class in `cloudglue/client/main.py`
5. Add the resource to `CloudGlue.__init__()`
6. Export from `cloudglue/client/resources/__init__.py`
