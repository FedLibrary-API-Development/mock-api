
def test_get_resources_empty(test_client):
    """Test getting all resources when none exist."""
    response = test_client.get("/api/v1/resources/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] == 0
    assert data["resources"] == []
    

def test_create_resource(test_client):
    """Test creating a new resource."""
    new_resource = {
        "title": "New API Resource",
        "description": "Created via API",
        "access_count": 467,
        "student_count": 32,
    }
    
    response = test_client.post("/api/v1/resources/", json=new_resource)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == new_resource["title"]
    assert data["description"] == new_resource["description"]
    assert data["access_count"] == new_resource["access_count"]
    assert data["student_count"] == new_resource["student_count"]
    # assert "id" in data  # ID should be generated
    
    # Verify resource was created
    resource_id = data["id"]
    response = test_client.get(f"/api/v1/resources/{resource_id}")
    assert response.status_code == 200


def test_create_resource_with_id(test_client):
    """Test creating a new resource with a specified ID."""
    new_resource = {
        "id": "custom-id-12345",
        "title": "Custom ID Resource",
        "description": "Resource with custom ID",
        "access_count": 782,
        "student_count": 102,
    }
    
    response = test_client.post("/api/v1/resources/", json=new_resource)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] == new_resource["id"]
    
    # Verify resource was created with the custom ID
    response = test_client.get(f"/api/v1/resources/{new_resource['id']}")
    assert response.status_code == 200


def test_get_resources(test_client, populate_test_csv, sample_resources):
    """Test getting all resources."""
    response = test_client.get("/api/v1/resources/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] == 2
    assert len(data["resources"]) == 2


def test_get_resource(test_client, populate_test_csv, sample_resources):
    """Test getting an resource by ID."""
    response = test_client.get(f"/api/v1/resources/{sample_resources[0]['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == sample_resources[0]["id"]
    assert data["title"] == sample_resources[0]["title"]
    assert data["description"] == sample_resources[0]["description"]
    assert data["access_count"] == sample_resources[0]["access_count"]
    assert data["student_count"] == sample_resources[0]["student_count"]


def test_get_resource_not_found(test_client):
    """Test getting a non-existent resource."""
    response = test_client.get("/api/v1/resources/non-existent-id")
    assert response.status_code == 404


def test_create_resource_validation_error(test_client):
    """Test creating an resource with invalid data."""
    # Missing required field
    invalid_resource = {
        "description": "Invalid resource"
    }
    
    response = test_client.post("/api/v1/resources/", json=invalid_resource)
    assert response.status_code == 422
    
    # Invalid access_count and student_count
    invalid_resource = {
        "title": "Invalid access_count and student_count Resource",
        "access_count": 0.76,
        "student_count": 1.102,
    }
    
    response = test_client.post("/api/v1/resources/", json=invalid_resource)
    assert response.status_code == 422


def test_update_resource(test_client, populate_test_csv, sample_resources):
    """Test updating an resource."""
    update_data = {
        "title": "Updated API Name",
        "access_count": 265,
        "student_count": 10,
    }
    
    response = test_client.put(f"/api/v1/resources/{sample_resources[0]['id']}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == sample_resources[0]["id"]
    assert data["title"] == update_data["title"]
    assert data["access_count"] == update_data["access_count"]
    assert data["student_count"] == update_data["student_count"]
    assert data["description"] == sample_resources[0]["description"]  # Unchanged
    
    # Verify resource was updated
    response = test_client.get(f"/api/v1/resources/{sample_resources[0]['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]


def test_update_resource_not_found(test_client):
    """Test updating a non-existent resource."""
    response = test_client.put("/api/v1/resources/non-existent-id", json={"title": "New Name"})
    assert response.status_code == 404


def test_delete_resource(test_client, populate_test_csv, sample_resources):
    """Test deleting an resource."""
    response = test_client.delete(f"/api/v1/resources/{sample_resources[0]['id']}")
    assert response.status_code == 200
    
    # Verify resource was deleted
    response = test_client.get(f"/api/v1/resources/{sample_resources[0]['id']}")
    assert response.status_code == 404


def test_delete_resource_not_found(test_client):
    """Test deleting a non-existent resource."""
    response = test_client.delete("/api/v1/resources/non-existent-id")
    assert response.status_code == 404