import pytest
from fastapi import HTTPException


def test_get_all_empty(test_repository):
    """Test getting all resources from an empty repository."""
    result = test_repository.get_all()
    assert result["count"] == 0
    assert result["resources"] == []


def test_get_all_with_resources(test_repository, populate_test_csv, sample_resources):
    """Test getting all resources with pagination."""
    result = test_repository.get_all()
    assert result["count"] == 3
    assert len(result["resources"]) == 3
    
    # Test pagination - skip
    result = test_repository.get_all(skip=1)
    assert result["count"] == 3
    assert len(result["resources"]) == 2
    assert result["resources"][0]["id"] == sample_resources[1]["id"]
    
    # Test pagination - limit
    result = test_repository.get_all(limit=1)
    assert result["count"] == 3
    assert len(result["resources"]) == 1
    assert result["resources"][0]["id"] == sample_resources[0]["id"]


def test_get_by_id(test_repository, populate_test_csv, sample_resources):
    """Test getting an resource by ID."""
    resource = test_repository.get_by_id(sample_resources[0]["id"])
    assert resource["id"] == sample_resources[0]["id"]
    assert resource["title"] == sample_resources[0]["title"]


def test_get_by_id_not_found(test_repository):
    """Test getting a non-existent resource."""
    with pytest.raises(HTTPException) as excinfo:
        test_repository.get_by_id("non-existent-id")
    assert excinfo.value.status_code == 404


def test_create_resource(test_repository):
    """Test creating a new resource."""
    new_resource = {
        "id": "new-resource-1",
        "title": "New Resource",
        "description": "Description for New Resource",
        "access_count": 752,
        "student_count": 47
    }
    
    result = test_repository.create(new_resource)
    assert result == new_resource
    
    # Verify resource was actually created
    resource = test_repository.get_by_id(new_resource["id"])
    assert resource["id"] == new_resource["id"]
    assert resource["title"] == new_resource["title"]


def test_create_resource_duplicate_id(test_repository, populate_test_csv, sample_resources):
    """Test creating an resource with a duplicate ID."""
    with pytest.raises(HTTPException) as excinfo:
        test_repository.create(sample_resources[0])
    assert excinfo.value.status_code == 400


def test_update_resource(test_repository, populate_test_csv, sample_resources):
    """Test updating an resource."""
    update_data = {
        "title": "Updated Name",
        "access_count": 1024,
        "student_count": 102,
    }
    
    result = test_repository.update(sample_resources[0]["id"], update_data)
    assert result["id"] == sample_resources[0]["id"]
    assert result["title"] == update_data["title"]
    assert result["access_count"] == update_data["access_count"]
    assert result["student_count"] == update_data["student_count"]  # Unchanged
    assert result["description"] == sample_resources[0]["description"]  # Unchanged
    
    # Verify resource was actually updated
    resource = test_repository.get_by_id(sample_resources[0]["id"])
    assert resource["title"] == update_data["title"]
    assert resource["access_count"] == update_data["access_count"]


def test_update_resource_not_found(test_repository):
    """Test updating a non-existent resource."""
    with pytest.raises(HTTPException) as excinfo:
        test_repository.update("non-existent-id", {"title": "Updated Name"})
    assert excinfo.value.status_code == 404


def test_delete_resource(test_repository, populate_test_csv, sample_resources):
    """Test deleting an resource."""
    result = test_repository.delete(sample_resources[0]["id"])
    assert "message" in result
    
    # Verify resource was actually deleted
    with pytest.raises(HTTPException) as excinfo:
        test_repository.get_by_id(sample_resources[0]["id"])
    assert excinfo.value.status_code == 404
    
    # Verify other resources still exist
    resource = test_repository.get_by_id(sample_resources[1]["id"])
    assert resource["id"] == sample_resources[1]["id"]


def test_delete_resource_not_found(test_repository):
    """Test deleting a non-existent resource."""
    with pytest.raises(HTTPException) as excinfo:
        test_repository.delete("non-existent-id")
    assert excinfo.value.status_code == 404