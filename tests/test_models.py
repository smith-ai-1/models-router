"""Tests for models endpoint."""



def test_models_endpoint_direct(test_client, mock_all_providers_env):
    """Test /v1/models endpoint directly."""
    response = test_client.get("/v1/models")

    assert response.status_code == 200
    data = response.json()

    assert data["object"] == "list"
    assert "data" in data
    assert len(data["data"]) > 0

    # Check first model structure
    model = data["data"][0]
    assert "id" in model
    assert "object" in model
    assert "created" in model
    assert "owned_by" in model
    assert model["object"] == "model"


def test_models_with_openai_client(
    openai_client_with_test_transport, mock_all_providers_env
):
    """Test models endpoint using OpenAI client with TestClient transport."""
    models = openai_client_with_test_transport.models.list()

    assert models.object == "list"
    assert len(models.data) > 0

    # Check that we have expected prefixed models
    model_ids = {model.id for model in models.data}
    assert "openai/gpt-3.5-turbo" in model_ids
    assert "openai/gpt-4" in model_ids
    assert "anthropic/claude-3-5-sonnet" in model_ids

    # Check model structure
    first_model = models.data[0]
    assert hasattr(first_model, "id")
    assert hasattr(first_model, "object")
    assert hasattr(first_model, "created")
    assert hasattr(first_model, "owned_by")
    assert first_model.object == "model"
