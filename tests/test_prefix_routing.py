"""Tests for prefix-based routing functionality."""

from unittest.mock import patch

from openai.types import CompletionUsage
from openai.types.chat import ChatCompletion, ChatCompletionMessage


def test_prefix_based_routing_openai(test_client, mock_openai_env):
    """Test routing with openai/ prefix."""
    with patch("src.model_router.providers.openai_provider.OpenAI") as mock_openai:
        # Mock response
        mock_response = ChatCompletion(
            id="test-123",
            choices=[{
                "finish_reason": "stop",
                "index": 0,
                "message": ChatCompletionMessage(
                    content="Hello from OpenAI!",
                    role="assistant",
                    refusal=None
                )
            }],
            created=1234567890,
            model="gpt-3.5-turbo",
            object="chat.completion",
            usage=CompletionUsage(
                completion_tokens=5,
                prompt_tokens=3,
                total_tokens=8
            )
        )

        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.return_value = mock_response

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
        assert data["choices"][0]["message"]["content"] == "Hello from OpenAI!"

        # Verify that the actual model name (without prefix) was sent to provider
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-3.5-turbo"  # No prefix


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

    # Should fail because groq provider create_chat_completion is not implemented yet
    assert response.status_code == 501  # NotImplementedError -> 501 Not Implemented
    assert "Groq provider not implemented yet" in response.json()["detail"]


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
    response = test_client.get("/v1/models")

    assert response.status_code == 200
    data = response.json()

    model_ids = [model["id"] for model in data["data"]]

    # Check prefixed models
    assert "openai/gpt-3.5-turbo" in model_ids
    assert "anthropic/claude-3-5-sonnet" in model_ids
    assert "groq/llama-3.1-70b" in model_ids
    assert "deepseek/deepseek-chat" in model_ids

    # All models should have prefixes now
    assert all("/" in model_id for model_id in model_ids)
