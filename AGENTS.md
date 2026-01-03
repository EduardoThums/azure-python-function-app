# AGENTS.md - Azure Functions Python Project

This document provides essential information for AI agents working on this Azure Functions Python project. Follow these guidelines to maintain consistency and quality.

## Project Overview

This is an Azure Functions project that uses Flask as the web framework, deployed to Azure Functions runtime. The project uses modern Python tooling including uv for dependency management and ruff for linting/formatting.

## Build/Lint/Test Commands

### Dependency Management
```bash
# Install dependencies (including dev dependencies)
uv sync

# Install dependencies without dev dependencies
uv sync --no-dev

# Update dependencies
uv lock --upgrade
```

### Linting and Formatting
```bash
# Run linter (ruff)
uv run ruff check .

# Run linter with auto-fix
uv run ruff check . --fix

# Format code (ruff)
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

### Local Development
```bash
# Start Azure Functions locally
func start

# Start on specific port
func start --port 7071
```

### Testing
**Note**: This project currently has no test suite. When adding tests:

```bash
# Run all tests (when pytest is added)
uv run pytest

# Run specific test file
uv run pytest tests/test_filename.py

# Run specific test function
uv run pytest tests/test_filename.py::test_function_name

# Run with coverage
uv run pytest --cov=.
```

### Deployment
```bash
# Deploy to Azure (from deploy.sh)
./deploy.sh

# Or manually prepare and deploy
func azure functionapp publish eduardoteste --no-build
```

## Code Style Guidelines

### Python Version
- **Required**: Python 3.13+
- Ensure compatibility with Python 3.13+ features

### Import Organization
```python
# Standard library imports (alphabetical)
import os
import json

# Third-party imports (alphabetical)
import azure.functions as func
from flask import Flask, Response

# Local imports (absolute paths preferred)
from . import module_name
```

### Naming Conventions
- **Functions/Methods**: `snake_case` (e.g., `get_user_data()`)
- **Variables**: `snake_case` (e.g., `user_name`)
- **Classes**: `PascalCase` (e.g., `UserService`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES = 3`)
- **Files**: `snake_case.py` (e.g., `user_service.py`)

### Type Hints
- Use type hints for all function parameters and return values
- Use `typing` module imports when needed

```python
from typing import Optional, List, Dict
import azure.functions as func

def process_request(req: func.HttpRequest) -> func.HttpResponse:
    # Function body
    pass
```

### Error Handling
- Use specific exception types rather than generic `Exception`
- Provide meaningful error messages
- Log errors appropriately

```python
try:
    # Risky operation
    result = risky_function()
except ValueError as e:
    # Handle specific error
    return func.HttpResponse(f"Invalid input: {str(e)}", status_code=400)
except Exception as e:
    # Handle unexpected errors
    return func.HttpResponse("Internal server error", status_code=500)
```

### Flask Route Patterns
```python
@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id: str):
    """Get user by ID."""
    # Implementation
    pass

@app.route("/api/users", methods=["POST"])
def create_user():
    """Create a new user."""
    # Implementation
    pass
```

### Azure Functions Patterns
```python
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Azure Functions entry point."""
    try:
        return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
    except Exception as e:
        context.log.error(f"Error processing request: {str(e)}")
        return func.HttpResponse("Internal server error", status_code=500)
```

### Docstrings
- Use triple quotes for all docstrings
- Follow Google/NumPy docstring format
- Include parameter and return value descriptions

```python
def calculate_total(items: List[Dict[str, float]]) -> float:
    """Calculate total price from a list of items.

    Args:
        items: List of dictionaries containing item data with 'price' key.

    Returns:
        Total price as a float.

    Raises:
        ValueError: If any item has invalid price data.
    """
    pass
```

### Logging
- Use the context logger provided by Azure Functions
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

```python
def process_data(req: func.HttpRequest, context: func.Context):
    context.log.info("Processing data request")
    try:
        # Processing logic
        context.log.debug("Data processed successfully")
        return func.HttpResponse("Success")
    except Exception as e:
        context.log.error(f"Error processing data: {str(e)}")
        return func.HttpResponse("Error", status_code=500)
```

### Security Best Practices
- Never log sensitive information (passwords, tokens, keys)
- Validate all input data
- Use parameterized queries if database operations are added
- Follow Azure Functions security guidelines

### File Structure
```
/
├── website/
│   ├── __init__.py          # Azure Functions entry point
│   ├── app.py              # Flask application
│   └── function.json       # Function configuration
├── host.json               # Host configuration
├── local.settings.json     # Local settings
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── .python-version         # Python version specification
└── deploy.sh              # Deployment script
```

### Configuration Files
- **pyproject.toml**: Project metadata, dependencies, and tool configurations
- **host.json**: Azure Functions host configuration
- **function.json**: Individual function configuration
- **local.settings.json**: Local development settings (not committed)

### Dependency Management
- Use `uv` for all dependency operations
- Specify version constraints in `pyproject.toml`
- Development dependencies in `[dependency-groups].dev` section
- Keep `uv.lock` file committed for reproducible builds

### Environment Variables
- Use `local.settings.json` for local development
- Access via `os.environ.get()` or Azure Functions configuration
- Never commit sensitive values

### Performance Considerations
- Minimize function cold starts
- Use appropriate Azure Functions plan
- Optimize imports and dependencies
- Consider caching strategies for frequently accessed data

### Testing Guidelines (Future Implementation)
When tests are added:
- Use `pytest` as the testing framework
- Place tests in `tests/` directory
- Use descriptive test names: `test_function_name_should_do_something`
- Mock external dependencies
- Include integration tests for Azure Functions
- Aim for >80% code coverage

### CI/CD
- GitHub Actions workflow handles deployment on main branch push
- Uses uv for dependency management in CI
- Deploys to Azure Functions App 'eduardoteste'

### Deployment Checklist
Before deploying:
1. Run `uv run ruff check .` - ensure no linting errors
2. Run `uv run ruff format --check .` - ensure code is formatted
3. Test locally with `func start` - verify functionality
4. Check `uv.lock` is up to date
5. Ensure no sensitive data in committed files

### Common Patterns to Avoid
- Global variables in function code
- Hardcoded configuration values
- Synchronous operations that should be asynchronous
- Large function bodies (break into smaller functions)
- Direct database queries in HTTP handlers (use service layer)

### Azure Functions Best Practices
- Keep functions stateless
- Use dependency injection where appropriate
- Handle CORS properly in production
- Configure appropriate authentication levels
- Use proper HTTP status codes
- Implement proper error responses

This document should be updated as the project evolves and new patterns emerge.</content>
<parameter name="filePath">/home/eduardo/workspace/azure-functions-terraform/AGENTS.md