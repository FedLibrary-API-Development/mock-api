
def test_missing_api_key(test_client_no_auth):
    """Test that requests without API key are rejected."""
    response = test_client_no_auth.get("/api/v1/resources/")
    assert response.status_code == 403
    assert "Invalid or missing API key" in response.json()["detail"]

def test_invalid_api_key(test_client):
    """Test that requests with invalid API key are rejected."""
    response = test_client.get("/api/v1/resources/", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 403
    assert "Invalid or missing API key" in response.json()["detail"]