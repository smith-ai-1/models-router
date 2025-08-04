"""Test configuration and fixtures."""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from openai import OpenAI

# Set testing environment before importing app
os.environ["TESTING"] = "true"

from model_router.main import app
from model_router.main_configuration import main_configuration, initialize_sample_data
import inject


@pytest.fixture(scope="session")
def initialized_config():
    """Initialize dependency injection configuration once per test session."""
    import asyncio
    
    # Configure dependency injection
    inject.configure_once(main_configuration)
    
    # Initialize sample data
    asyncio.run(initialize_sample_data())
    
    return True


@pytest.fixture
def test_client(initialized_config):
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_openai_env():
    """Mock OpenAI environment variable."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        yield


@pytest.fixture
def mock_all_providers_env():
    """Mock all provider environment variables."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "GROQ_API_KEY": "test-groq-key",
        "DEEPSEEK_API_KEY": "test-deepseek-key",
    }):
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
