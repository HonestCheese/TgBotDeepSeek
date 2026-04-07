from pathlib import Path
from PIL import Image
from pydantic import EmailStr

from tasks.celery_app import celery
from tasks.email_templates import email_registration_template

import smtplib


@celery.task
def process_pic(path: str):
    path = Path(path)
    img = Image.open(path)
    img = img.resize((100, 100))

    # Сохраняем в WEBP - поддерживает все режимы включая RGBA
    output_path = f"static/images/resized_{path.stem}.webp"
    img.save(output_path, 'WEBP', quality=85)


@celery.task
def send_email(
        email: EmailStr,
):
    email_mock = "gubskii.md@gmail.com"
    msg_content = email_registration_template(email_mock)
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login("gubskii.md@gmail.com", "nkgy unre mjyt andg")
        smtp.send_message(msg_content)
    return {"status": "sent", "to": email}

@celery.task
def test_task():
    return {"message": "Hello from Celery!", "status": "success"}