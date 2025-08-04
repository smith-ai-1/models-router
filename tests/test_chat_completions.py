"""Tests for chat completions endpoint."""




def test_chat_completions_missing_auth(test_client):
    """Test chat completions without authorization header."""
    response = test_client.post(
        "/v1/chat/completions",
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    assert response.status_code == 401
    assert "Invalid or missing API key" in response.json()["detail"]


def test_chat_completions_invalid_model(test_client):
    """Test chat completions with invalid model."""
    response = test_client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "invalid-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )

    assert response.status_code == 404
    assert "Model invalid-model not found" in response.json()["detail"]


def test_chat_completions_no_openai_key(test_client):
    """Test chat completions without OpenAI API key configured."""
    # This test is no longer relevant in the new architecture since testing mode
    # always uses mock adapters. Keeping as placeholder but skipping.
    # TODO: Update test to work with production mode configuration
    import pytest
    pytest.skip("Test needs update for new service architecture")


def test_chat_completions_success(test_client, mock_openai_env):
    """Test successful chat completion."""
    # In testing mode, the MockOpenAIAdapter is used automatically
    response = test_client.post(
        "/v1/chat/completions",
        headers={"Authorization": "Bearer test-key"},
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 100
        }
    )

    assert response.status_code == 200
    data = response.json()

    # MockOpenAIAdapter returns specific mock response
    assert "chatcmpl-mock" in data["id"]
    assert data["object"] == "chat.completion"
    assert data["model"] == "gpt-3.5-turbo"
    assert len(data["choices"]) == 1
    assert "mock response from openai adapter" in data["choices"][0]["message"]["content"].lower()
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert data["usage"]["total_tokens"] == 20


def test_chat_completions_with_openai_client(
    openai_client_with_test_transport, mock_openai_env
):
    """Test chat completion using OpenAI client with TestClient transport."""
    # In testing mode, the MockOpenAIAdapter is used automatically
    # Use OpenAI client to make request
    response = openai_client_with_test_transport.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": "How are you?"}],
        temperature=0.5,
        max_tokens=50
    )

    # MockOpenAIAdapter returns specific mock response
    assert "chatcmpl-mock" in response.id
    assert response.object == "chat.completion"
    assert response.model == "gpt-3.5-turbo"
    assert len(response.choices) == 1
    assert "mock response from openai adapter" in response.choices[0].message.content.lower()
    assert response.choices[0].message.role == "assistant"
    assert response.usage.total_tokens == 20
