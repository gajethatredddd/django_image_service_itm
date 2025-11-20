import pytest
from unittest.mock import patch, AsyncMock

def test_email_form_page(client):
    """Test email form page loads"""
    response = client.get("/api/v1/emails/form")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_task_status_endpoint(client):
    """Test task status endpoint"""
    response = client.get("/api/v1/emails/task-status/test-task-id")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data

def test_email_form_submit_validation_error(client):
    """Test form submit with validation error"""
    response = client.post("/api/v1/emails/form-submit", data={
        # Missing required fields
    })
    assert response.status_code == 422

def test_available_ids_endpoint_integration(client):
    """Test available IDs endpoint (integration test)"""
    # This will actually call the real endpoint
    response = client.get("/api/v1/emails/available-ids")
    assert response.status_code == 200
    data = response.json()
    # Should have available_ids field, even if empty
    assert "available_ids" in data

def test_email_form_submit_missing_id(client):
    """Test form submit with missing ID - should return 422"""
    response = client.post("/api/v1/emails/form-submit", data={
        "email_to": "test@example.com",
        "include_image": "false"
    })
    # FastAPI returns 422 for validation errors
    assert response.status_code == 422

def test_email_form_submit_invalid_data(client):
    """Test form submit with invalid data"""
    response = client.post("/api/v1/emails/form-submit", data={
        "item_id": "not-a-number",
        "email_to": "not-an-email",
        "include_image": "false"
    })
    assert response.status_code == 422