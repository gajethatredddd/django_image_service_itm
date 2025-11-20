from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI
    app_name: str = "Image Analysis Email Service"
    debug: bool = False

    # Email
    email_from: str
    email_password: str
    smtp_server: str = "smtp.mail.ru"
    smtp_port: int = 465

    # Django API
    django_api_url: str = "http://web:8000/api/v1"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()