"""Tests for user endpoint."""


def test_get_current_user_success(test_client, initialized_config):
    """Test getting current user information with valid token."""
    response = test_client.get(
        "/v1/user/me",
        headers={"Authorization": "Bearer admin-token-123"}
    )

    assert response.status_code == 200
    data = response.json()
    
    assert "uid" in data
    assert data["email"] == "admin@example.com"
    assert data["additional_info"]["role"] == "admin"
    assert "created_at" in data
    assert "updated_at" in data


def test_get_current_user_invalid_token(test_client, initialized_config):
    """Test getting current user with invalid token."""
    response = test_client.get(
        "/v1/user/me",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]


def test_get_current_user_no_auth(test_client, initialized_config):
    """Test getting current user without authorization header."""
    response = test_client.get("/v1/user/me")

    assert response.status_code == 401
    assert "Invalid or missing API key" in response.json()["detail"]


def test_get_current_user_developer_token(test_client, initialized_config):
    """Test getting current user with developer token."""
    response = test_client.get(
        "/v1/user/me",
        headers={"Authorization": "Bearer dev-token-456"}
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["email"] == "developer@example.com"
    assert data["additional_info"]["role"] == "developer"