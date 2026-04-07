from email.message import EmailMessage

from pydantic  import EmailStr


def email_registration_template(
         email_to: EmailStr,
):
    msg = EmailMessage()
    msg["From"] = "gubskii.md@gmail.com"
    msg["To"] = "lolpolmiki228@gmail.com"
    msg["Subject"] = "TEST AHAHHHAHAHAHA"
    msg.set_content("Привет! Это тестовое письмо.")
    return msg