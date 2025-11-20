import smtplib
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.core.celery import celery_app
from app.core.config import settings


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, item_id: int, email_to: str, include_image: bool = False):
    try:
        with httpx.Client() as client:
            response = client.get(f"{settings.django_api_url}/lol/{item_id}/")
            if response.status_code == 404:
                return {
                    "status": "error",
                    "message": f"Image with ID {item_id} not found",
                    "item_id": item_id,
                    "email_to": email_to
                }
            response.raise_for_status()
            data = response.json()
            extracted_text = data.get("extracted_text", "Text not found")

            image_data = None
            image_mime_type = "image/jpeg"
            if include_image:
                image_url = data.get('path')
                if image_url:
                    image_response = client.get(image_url)
                    if image_response.status_code == 200:
                        image_data = image_response.content
                        # Определяем MIME тип
                        if image_url.lower().endswith('.png'):
                            image_mime_type = 'image/png'
                        elif image_url.lower().endswith('.jpg') or image_url.lower().endswith('.jpeg'):
                            image_mime_type = 'image/jpeg'

        # Создаем email сообщение
        if include_image and image_data:
            msg = MIMEMultipart()
            text_part = MIMEText(f"""
Текст с картинки #{item_id}

{extracted_text}

---
Отправлено из Image Analysis Service
            """)
            msg.attach(text_part)

            image_attachment = MIMEImage(image_data, _subtype=image_mime_type.split('/')[1])
            image_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=f'image_{item_id}.{image_mime_type.split("/")[1]}'
            )
            msg.attach(image_attachment)
            subject = f'Текст и картинка #{item_id}'
        else:
            msg = MIMEText(f"""
Текст с картинки #{item_id}

{extracted_text}

---
Отправлено из Image Analysis Service
            """)
            subject = f'Текст с картинки #{item_id}'

        msg['Subject'] = subject
        msg['From'] = settings.email_from
        msg['To'] = email_to

        # Отправляем email
        server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=30)
        server.login(settings.email_from, settings.email_password)
        server.send_message(msg)
        server.quit()

        return {
            "status": "success",
            "message": f"Email sent for ID {item_id} to {email_to}",
            "item_id": item_id,
            "email_to": email_to,
            "image_included": include_image and image_data is not None
        }

    except Exception as e:
        self.retry(countdown=60, exc=e)
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "item_id": item_id,
            "email_to": email_to
        }