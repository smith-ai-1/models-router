# Claude Code Instructions

This file contains specific instructions and context for Claude Code when working on this project.

## Project Overview

This is a Model Router service that provides an OpenAI-compatible API for routing requests to multiple AI providers (OpenAI, Anthropic, Groq, DeepSeek). The service uses prefix-based routing to determine which provider to use for each model.

## Development Workflow

Follow the comprehensive development workflow documented in [.ai/workflows/dev_workflow.md](./.ai/workflows/dev_workflow.md). Key principles:

1. **Use TodoWrite tool** for complex multi-step tasks
2. **Follow existing patterns** by reading code before implementing
3. **Write comprehensive tests** using pytest and FastAPI TestClient
4. **Run linting and tests** before committing changes
5. **Commit with clear messages** and proper attribution

## Architecture

- **FastAPI application** with OpenAI-compatible endpoints (`/v1/models`, `/v1/chat/completions`)
- **Provider pattern** with abstract base class and concrete implementations
- **Prefix-based routing** using `provider/model-name` format
- **Dynamic model listing** from provider instances rather than static configuration

## Testing Strategy

- Use real SDK integrations (OpenAI client with TestClient transport)
- Mock only external API calls, not the entire provider chain
- Include comprehensive error handling and edge case testing
- Test both individual providers and multi-provider scenarios

## Code Standards

- Python 3.13+ with modern syntax (union types with `|`)
- Ruff linting with 88 character line limit
- Type hints for all functions
- No comments unless explicitly requested
- Follow existing import and code organization patterns

## Common Commands

```bash
# Development
python run_server.py
uv run pytest tests/ -v
uv run ruff check --fix

# Git workflow
git add . && git commit -m "..." && git push origin main
```

## Key Files

- `src/model_router/main.py` - FastAPI application and routing logic
- `src/model_router/providers/` - Provider implementations
- `tests/` - Comprehensive test suite
- `.env.example` - Environment variables template
- `pyproject.toml` - Project configuration and dependencies

## Environment Variables

All providers require API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY` 
- `GROQ_API_KEY`
- `DEEPSEEK_API_KEY`

## Testing Notes

- Use `mock_all_providers_env` fixture for tests requiring all providers
- Use `mock_openai_env` for OpenAI-specific tests
- TestClient automatically handles httpx requests for OpenAI SDK integration
- Provider placeholders (Anthropic, Groq, DeepSeek) return NotImplementedError