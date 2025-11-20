from celery import Celery
import smtplib
from email.mime.text import MIMEText
import httpx

celery_app = Celery(
    'fastapi_worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

EMAIL_FROM = "Letsmc@mail.ru"
EMAIL_PASSWORD = "sULXZuZSxQtHlVY7Jq7W"


@celery_app.task
def send_email_task(item_id: int, email_to: str):

    try:

        with httpx.Client() as client:
            response = client.get(f"http://web:8000/api/v1/lol/{item_id}/")
            response.raise_for_status()
            data = response.json()
            extracted_text = data.get("extracted_text", "Текст не найден")

        msg = MIMEText(f"""
Текст с картинки #{item_id}

{extracted_text}

---
Отправлено из моего приложения крутого
        """)

        msg['Subject'] = f'Текст с картинки #{item_id}'
        msg['From'] = EMAIL_FROM
        msg['To'] = email_to

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465, timeout=30)
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return {
            "status": "success",
            "message": f"Email sent for ID {item_id} to {email_to}",
            "item_id": item_id,
            "email_to": email_to
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "item_id": item_id,
            "email_to": email_to
        }