import time
from app.core.config import settings
from app.core.exceptions import EmailServiceError
from app.services.tasks import send_email_task


class EmailService:
    def __init__(self):
        self.last_sent_time = 0

    async def send_email_async(
            self,
            item_id: int,
            email_to: str,
            include_image: bool = False
    ) -> str:
        """Асинхронная отправка через Celery"""
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_sent_time < 5:
            raise EmailServiceError("Rate limit: wait 5 seconds between emails")

        self.last_sent_time = current_time

        # Запускаем фоновую задачу
        task = send_email_task.delay(item_id, email_to, include_image)

        return task.id