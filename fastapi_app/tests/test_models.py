from app.domain.models import HealthResponse, EmailRequest


def test_health_response_model():
    """Test HealthResponse model"""
    health_data = {
        "status": "healthy",
        "service": "Test Service",
        "timestamp": "2024-01-01T00:00:00"
    }
    health_response = HealthResponse(**health_data)

    assert health_response.status == "healthy"
    assert health_response.service == "Test Service"
    assert health_response.timestamp == "2024-01-01T00:00:00"


def test_email_request_model():
    """Test EmailRequest model"""
    email_data = {
        "item_id": 1,
        "email_to": "test@example.com",
        "include_image": True
    }
    email_request = EmailRequest(**email_data)

    assert email_request.item_id == 1
    assert email_request.email_to == "test@example.com"
    assert email_request.include_image == True


def test_email_request_defaults():
    """Test EmailRequest model defaults"""
    email_data = {
        "item_id": 1,
        "email_to": "test@example.com"
    }
    email_request = EmailRequest(**email_data)

    assert email_request.include_image == False  # default value