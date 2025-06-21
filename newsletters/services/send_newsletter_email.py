from django.core.mail import send_mail
from newsletters.models import MailingAttempt
from dotenv import load_dotenv

import os

load_dotenv()

def send_newsletter_email(mailing, recipient_email):
    """ Функция для отправки письма с фиксацией попытки """
    try:

        subject = mailing.message.title
        message = mailing.message.content
        from_email = os.getenv('EMAIL_HOST_USER')

        send_mail(subject, message, from_email, [recipient_email])

        # Если успешно — создаем запись о попытке
        MailingAttempt.objects.create(
            mailing=mailing,
            status='success',
            server_response='Письмо успешно отправлено'
        )
        return True
    except Exception as e:
        # В случае ошибки — создаем запись о неуспешной попытке
        MailingAttempt.objects.create(
            mailing=mailing,
            status='failure',
            server_response=str(e)
        )
        return False
