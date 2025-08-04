"""Tests for prefix-based routing functionality."""



def test_prefix_based_routing_openai(test_client, mock_openai_env):
    """Test routing with openai/ prefix."""
    # In testing mode, the MockOpenAIAdapter is used automatically
    response = test_client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    assert response.status_code == 200
    data = response.json()
    # MockOpenAIAdapter returns specific mock response
    assert "chatcmpl-mock" in data["id"]
    assert data["object"] == "chat.completion"
    assert data["model"] == "gpt-3.5-turbo"  # Model name without prefix
    assert "mock response from openai adapter" in data["choices"][0]["message"]["content"].lower()


def test_groq_routing_works(test_client, mock_all_providers_env):
    """Test that groq prefix routing works."""
    response = test_client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "groq/llama-3.1-70b",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    # In testing mode, MockGroqAdapter returns successful response
    assert response.status_code == 200
    data = response.json()
    assert "chatcmpl-mock-groq" in data["id"]
    assert data["object"] == "chat.completion"
    assert data["model"] == "llama-3.1-70b"
    assert "mock response from groq adapter" in data["choices"][0]["message"]["content"].lower()


def test_invalid_model_prefix(test_client):
    """Test error handling for invalid model prefix."""
    response = test_client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "invalid/unknown-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    assert response.status_code == 404
    assert "Model invalid/unknown-model not found" in response.json()["detail"]


def test_model_list_includes_prefixed_models(test_client, mock_all_providers_env):
    """Test that model list includes only prefixed models."""
    response = test_client.get("/v1/models", headers={"Authorization": "Bearer test-key"})

    assert response.status_code == 200
    data = response.json()

    model_ids = [model["id"] for model in data["data"]]

    # Check prefixed models
    assert "openai/gpt-3.5-turbo" in model_ids
    assert any("anthropic/claude-3-5-sonnet" in model_id for model_id in model_ids)
    assert "groq/llama-3.1-70b-versatile" in model_ids
    assert "deepseek/deepseek-chat" in model_ids

    # All models should have prefixes now
    assert all("/" in model_id for model_id in model_ids)
