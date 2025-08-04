# Development Workflow

This document describes the recommended development workflow for the Model Router project.

## Feature Development Process

### 1. Planning Phase
- Use the `TodoWrite` tool to create a task list for complex features
- Break down the feature into specific, actionable items
- Set appropriate priorities (high/medium/low)
- Mark tasks as `in_progress` when starting work

### 2. Implementation Phase
- **Follow existing patterns**: Always examine existing code to understand conventions
- **Check dependencies**: Use `grep` or `search` to verify libraries are already in use
- **Maintain consistency**: Follow the established architecture patterns
- **Code without comments**: Only add comments when explicitly requested

### 3. Testing Phase
- **Write comprehensive tests**: Use pytest with FastAPI TestClient
- **Use real integrations**: Integrate with actual SDKs (like OpenAI client) through TestClient
- **Mock only when necessary**: Prefer real implementations over mocks when possible
- **Test edge cases**: Include error handling, validation, and boundary conditions

### 4. Quality Assurance
- **Run linting**: Always execute `uv run ruff check --fix` before committing
- **Run tests**: Execute `uv run pytest tests/ -v` to ensure all tests pass
- **Fix formatting**: Address all ruff warnings and errors
- **Verify functionality**: Test the actual API endpoints work as expected

### 5. Git Workflow
- **Staged commits**: Add all changes with `git add .`
- **Descriptive messages**: Write clear commit messages explaining the changes
- **Push immediately**: Push changes after successful commit

## Architecture

See [architecture.md](./architecture.md) for detailed architectural principles, patterns, and design decisions.

## Code Standards

### Python Style
- Use Python 3.13+ features (union types with `|`)
- Follow ruff configuration (88 character line limit)
- Use type hints for all function parameters and returns
- Prefer explicit imports over wildcard imports

### FastAPI Patterns
- Use Pydantic models for request/response validation
- Include proper HTTP status codes and error messages
- Document endpoints with clear docstrings
- Handle exceptions with appropriate HTTP responses

### Project Structure
```
src/model_router/
├── main.py              # FastAPI application and routing
├── providers/           # Provider implementations
│   ├── base.py         # Abstract base class
│   ├── openai_provider.py
│   └── ...
tests/
├── conftest.py         # Test fixtures and configuration
├── test_*.py           # Test modules
└── ...
```

## Common Commands

### Development
```bash
# Install dependencies
uv sync

# Run server in development
python run_server.py

# Run tests
uv run pytest tests/ -v

# Lint and format
uv run ruff check --fix
```

### Git Operations
```bash
# Check status and diff
git status && git diff

# Commit with attribution
git add . && git commit -m "feat: description"

# Push changes
git push origin main
```

## Best Practices

1. **Always read before writing**: Use `Read` tool to understand existing code
2. **Test-driven development**: Write tests alongside implementation
3. **Incremental commits**: Commit logical units of work
4. **Error handling**: Provide meaningful error messages and proper HTTP codes
5. **Documentation**: Keep this workflow updated as patterns evolve

## Troubleshooting

### Common Issues
- **Import errors**: Verify all dependencies are properly installed with `uv sync`
- **Test failures**: Check fixture dependencies and environment variables
- **Linting errors**: Run `uv run ruff check --fix` to auto-fix most issues
- **Type errors**: Ensure all functions have proper type annotations

### Debug Commands
```bash
# Check Python environment
uv run python --version

# Verify package installation
uv run pip list

# Run specific test file
uv run pytest tests/test_specific.py -v

# Check code without fixing
uv run ruff check
```