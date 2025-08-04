"""Tests for chat completions endpoint."""

from unittest.mock import patch

from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion, ChatCompletionMessage


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
    with patch.dict('os.environ', {}, clear=True):
        response = test_client.post(
            "/v1/chat/completions",
            headers={"Authorization": "Bearer test-key"},
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )

    assert response.status_code == 401
    assert "OpenAI API key not configured" in response.json()["detail"]


@patch("src.model_router.providers.openai_provider.OpenAI")
def test_chat_completions_success(mock_openai_class, test_client, mock_openai_env):
    """Test successful chat completion."""
    # Mock OpenAI response
    mock_response = ChatCompletion(
        id="chatcmpl-test123",
        choices=[{
            "finish_reason": "stop",
            "index": 0,
            "message": ChatCompletionMessage(
                content="Hello! How can I help you today?",
                role="assistant",
                refusal=None
            )
        }],
        created=1234567890,
        model="gpt-3.5-turbo",
        object="chat.completion",
        usage=CompletionUsage(
            completion_tokens=10,
            prompt_tokens=5,
            total_tokens=15
        )
    )

    # Configure mock
    mock_client = mock_openai_class.return_value
    mock_client.chat.completions.create.return_value = mock_response

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

    assert data["id"] == "chatcmpl-test123"
    assert data["object"] == "chat.completion"
    assert data["model"] == "gpt-3.5-turbo"
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["content"] == (
        "Hello! How can I help you today?"
    )
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert data["usage"]["total_tokens"] == 15

    # Verify OpenAI client was called correctly
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stream=False,
        stop=None,
        n=1
    )


@patch("src.model_router.providers.openai_provider.OpenAI")
def test_chat_completions_with_openai_client(
    mock_openai_class, openai_client_with_test_transport, mock_openai_env
):
    """Test chat completion using OpenAI client with TestClient transport."""
    # Mock OpenAI response
    mock_response = ChatCompletion(
        id="chatcmpl-test456",
        choices=[{
            "finish_reason": "stop",
            "index": 0,
            "message": ChatCompletionMessage(
                content="I'm doing well, thank you!",
                role="assistant",
                refusal=None
            )
        }],
        created=1234567890,
        model="gpt-3.5-turbo",
        object="chat.completion",
        usage=CompletionUsage(
            completion_tokens=8,
            prompt_tokens=6,
            total_tokens=14
        )
    )

    # Configure mock
    mock_client = mock_openai_class.return_value
    mock_client.chat.completions.create.return_value = mock_response

    # Use OpenAI client to make request
    response = openai_client_with_test_transport.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": "How are you?"}],
        temperature=0.5,
        max_tokens=50
    )

    assert response.id == "chatcmpl-test456"
    assert response.object == "chat.completion"
    assert response.model == "gpt-3.5-turbo"
    assert len(response.choices) == 1
    assert response.choices[0].message.content == "I'm doing well, thank you!"
    assert response.choices[0].message.role == "assistant"
    assert response.usage.total_tokens == 14

    # Verify the underlying OpenAI client was called
    mock_client.chat.completions.create.assert_called_once()
