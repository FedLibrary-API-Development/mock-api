import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.db import ResourceRepository
from app.core import settings

@pytest.fixture
def test_api_key():
    """Fixture for test API key."""
    return "test-api-key-12345"


@pytest.fixture(autouse=True)
def setup_test_api_keys(test_api_key):
    """Setup API keys for testing environment."""
    # Save original API keys
    original_keys = getattr(settings, 'API_KEYS', []).copy() if hasattr(settings, 'API_KEYS') else []
    
    # Set test API key
    settings.API_KEYS = [test_api_key]
    
    yield
    
    # Restore original keys
    settings.API_KEYS = original_keys
    
    
@pytest.fixture
def test_client_no_auth():
    """Fixture for FastAPI test client without authentication."""
    with TestClient(app) as client:
        # Explicitly don't add any auth headers
        yield client


@pytest.fixture
def test_csv_path():
    """Fixture for test CSV file path"""
    
    test_path = "tests/data/test_resources.csv"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    
    # Create empty CSV file with expected columns
    df = pd.DataFrame(columns=ResourceRepository.COLUMNS)
    df.to_csv(test_path, index=False)
    
    yield test_path
    
    # Clean up - remove test file
    if os.path.exists(test_path):
        os.remove(test_path)
        

@pytest.fixture
def test_repository(test_csv_path):
    """Fixture for test repository."""
    return ResourceRepository(file_path=test_csv_path)


@pytest.fixture
def test_client(test_api_key):
    """Fixture for FastAPI test client."""
    with TestClient(app) as client:
        # Add API key to default headers
        client.headers.update({"X-API-Key": test_api_key})
        yield client
        
        
@pytest.fixture
def sample_resources():
    """Fixture for sample resources."""
    return [
        {
            "id": "custom-id-12345",
            "title": "Custom ID Resource",
            "description": "Resource with custom ID",
            "access_count": 782,
            "student_count": 102,
        },
        {
            "id": "test-resource-1",
            "title": "Test Resource 1",
            "description": "Description for Test Resource 1",
            "access_count": 582,
            "student_count": 47
        },
        {
            "id": "test-resource-2",
            "title": "Test Resource 2",
            "description": "Description for Test Resource 2",
            "access_count": 967,
            "student_count": 94
        }
    ]
    
    
@pytest.fixture
def populate_test_csv(test_csv_path, sample_resources):
    """Fixture to populate test CSV with sample resources."""
    df = pd.DataFrame(sample_resources)
    df.to_csv(test_csv_path, index=False)
    return sample_resources