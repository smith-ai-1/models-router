# Architecture Principles

This document outlines the core architectural patterns and principles for the Model Router project.

## Provider Pattern

### Base Provider Interface
- Each AI provider should extend `BaseProvider`
- Implement `get_available_models()` and `create_chat_completion()`
- Use dependency injection for API keys
- Handle provider-specific errors appropriately

### Provider Implementation
```python
class CustomProvider(BaseProvider):
    def get_available_models(self) -> list[str]:
        return ["model-1", "model-2"]
    
    async def create_chat_completion(self, **kwargs) -> ChatCompletion:
        # Provider-specific implementation
        pass
```

### Provider Registration
- Add provider to `PROVIDER_PREFIXES` mapping
- Include API key validation in `get_provider()` function
- Handle `NotImplementedError` for incomplete providers

## Prefix-based Routing

### Model Naming Convention
- All models use provider prefixes: `provider/model-name`
- Examples: `openai/gpt-4`, `anthropic/claude-3-5-sonnet`
- Strip prefixes when sending requests to actual providers
- Validate model existence before routing

### Routing Logic
1. Parse model name to extract provider prefix
2. Look up provider in `PROVIDER_PREFIXES` mapping
3. Get provider instance with API key validation
4. Strip prefix from model name
5. Route request to provider implementation

## API Design

### OpenAI Compatibility
- Implement `/v1/models` and `/v1/chat/completions` endpoints
- Use identical request/response formats as OpenAI API
- Support all standard parameters (temperature, max_tokens, etc.)
- Return proper HTTP status codes and error messages

### Dynamic Model Discovery
- Models are discovered dynamically from provider instances
- `/v1/models` endpoint queries all configured providers
- Only shows models from providers with valid API keys
- Automatically adds provider prefixes to model IDs

## Testing Strategy

### Test Architecture
- Use `mock_all_providers_env` fixture for multi-provider tests
- Use `mock_openai_env` for OpenAI-specific tests
- Create separate test files for different concerns
- Test both direct API calls and SDK integration

### Integration Testing
- Use FastAPI TestClient with real OpenAI SDK
- Mock only external API calls, not internal routing
- Test complete request/response cycles
- Include negative test cases (invalid models, missing keys, etc.)

### Test Organization
```
tests/
├── conftest.py              # Fixtures and test configuration
├── test_models.py           # Model listing tests
├── test_chat_completions.py # Chat completion tests
├── test_prefix_routing.py   # Routing logic tests
└── test_providers.py        # Provider-specific tests
```

## Error Handling

### HTTP Status Codes
- `401 Unauthorized`: Missing or invalid API keys
- `404 Not Found`: Invalid model or provider
- `501 Not Implemented`: Provider not yet implemented
- `500 Internal Server Error`: Unexpected errors

### Error Response Format
```json
{
  "detail": "Human-readable error message"
}
```

## Configuration Management

### Environment Variables
- Each provider requires its own API key
- Use descriptive variable names: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
- Validate API keys at provider instantiation
- Gracefully handle missing keys (skip provider)

### Provider Configuration
- Centralized provider mapping in `PROVIDER_PREFIXES`
- Lazy loading of provider instances
- Fail-fast validation for critical configuration

## Extensibility

### Adding New Providers
1. Create provider class extending `BaseProvider`
2. Implement required abstract methods
3. Add provider prefix to `PROVIDER_PREFIXES`
4. Update `get_provider()` function
5. Add environment variable for API key
6. Write provider-specific tests

### Adding New Endpoints
- Follow OpenAI API specification for compatibility
- Use Pydantic models for request/response validation
- Include comprehensive error handling
- Add corresponding test coverage

## Performance Considerations

### Caching Strategy
- Provider instances are created per request (stateless)
- Model lists are generated dynamically (no caching)
- Consider adding caching for model discovery in production

### Async Pattern
- All provider methods are async for non-blocking I/O
- Use proper async/await throughout the request pipeline
- Handle async errors with try/catch blocks

## Security

### API Key Management
- Never log or expose API keys
- Validate API keys at provider boundary
- Use environment variables for configuration
- Implement proper error messages without key exposure

### Request Validation
- Use Pydantic models for strict request validation
- Validate all input parameters
- Sanitize error messages to prevent information leakage