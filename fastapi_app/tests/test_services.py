import pytest
from unittest.mock import patch, MagicMock
from app.services.tasks import send_email_task


def test_send_email_task_success():
    """Test successful email sending task"""
    with patch('app.services.tasks.httpx.Client') as mock_client, \
            patch('app.services.tasks.smtplib.SMTP_SSL') as mock_smtp:
        # Mock Django API response
        mock_django_response = MagicMock()
        mock_django_response.status_code = 200
        mock_django_response.json.return_value = {
            "extracted_text": "test text",
            "path": "http://example.com/image.jpg"
        }

        # Mock image download response
        mock_image_response = MagicMock()
        mock_image_response.status_code = 200
        mock_image_response.content = b"fake image data"

        mock_client.return_value.__enter__.return_value.get.side_effect = [
            mock_django_response,
            mock_image_response
        ]

        # Mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        # Execute task
        result = send_email_task(1, "test@example.com", True)

        assert result["status"] == "success"
        assert "Email sent" in result["message"]
        assert result["image_included"] == True


def test_send_email_task_text_only():
    """Test email task without image"""
    with patch('app.services.tasks.httpx.Client') as mock_client, \
            patch('app.services.tasks.smtplib.SMTP_SSL') as mock_smtp:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "extracted_text": "test text",
            "path": "http://example.com/image.jpg"
        }

        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        result = send_email_task(1, "test@example.com", False)

        assert result["status"] == "success"
        assert result["image_included"] == False


def test_send_email_task_image_not_found():
    """Test email task when image not found"""
    with patch('app.services.tasks.httpx.Client') as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        result = send_email_task(999, "test@example.com", True)

        assert result["status"] == "error"
        assert "not found" in result["message"].lower()


def test_send_email_task_smtp_error():
    """Test email task with SMTP error"""
    with patch('app.services.tasks.httpx.Client') as mock_client, \
            patch('app.services.tasks.smtplib.SMTP_SSL') as mock_smtp:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "extracted_text": "test text",
            "path": "http://example.com/image.jpg"
        }

        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        # Mock SMTP to raise exception
        mock_smtp.return_value.__enter__.side_effect = Exception("SMTP connection failed")

        result = send_email_task(1, "test@example.com", False)

        # Now it should return status: error
        assert result["status"] == "error"
        assert "SMTP" in result["error"]