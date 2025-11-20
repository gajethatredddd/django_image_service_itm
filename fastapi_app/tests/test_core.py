from app.core.config import settings

def test_settings_loaded():
    """Test that settings are loaded correctly"""
    assert settings.app_name == "Image Analysis Email Service"
    assert settings.debug == False
    assert settings.smtp_server == "smtp.mail.ru"
    assert settings.smtp_port == 465

def test_celery_app_creation():
    """Test that Celery app can be created"""
    from app.core.celery import celery_app
    assert celery_app is not None
    assert hasattr(celery_app, 'send_task')