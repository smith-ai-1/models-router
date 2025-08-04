"""Test configuration and fixtures."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from openai import OpenAI
import httpx

from src.model_router.main import app


@pytest.fixture
def test_client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_openai_env():
    """Mock OpenAI environment variable."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def openai_client_with_test_transport(test_client):
    """OpenAI client using FastAPI TestClient."""
    
    # Create OpenAI client with TestClient as httpx client
    client = OpenAI(
        base_url="http://testserver/v1", 
        api_key="test-key",
        http_client=test_client
    )
    
    return client