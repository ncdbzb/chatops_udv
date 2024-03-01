import smtplib
from email.message import EmailMessage

from config.config import SMTP_PASSWORD, SMTP_USER


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


def get_verify_email_template(name: str, user_email: str, token: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Подтвердите свой аккаунт'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Чтобы пройти верификацию, перейдите по <b>ссылке</b></p>'
        f'<p>http://localhost:8000/auth/verify/{token}</p>'
        '</div>',
        subtype='html'
    )
    return email


def get_forgot_email_template(name: str, user_email: str, token: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Сброс пароля'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Чтобы сбросить пароль, перейдите по <b>ссылке</b></p>'
        f'<p>http://localhost:8000/auth/reset-password/{token}</p>'
        '</div>',
        subtype='html'
    )
    return email


def send_email(name: str, user_email: str,  token: str, destiny: str):
    if destiny == 'verify':
        email = get_verify_email_template(name, user_email, token)
    elif destiny == 'forgot':
        email = get_forgot_email_template(name, user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
    return {
         "status_code": 200,
         "data": "Письмо отправлено",
         "details": None
    }
