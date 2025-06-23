import os

from django.core.mail import send_mail
from dotenv import load_dotenv

from mailings.models import MailingRecipient

from .models import Mailing, MessageLog

load_dotenv()


def send_mailing(mailing_id):
    """Функция, которая проходит по выбранной рассылке и отправляет письма каждому получателю, логируя результат"""
    mailing = Mailing.objects.get(id=mailing_id)
    if not mailing.is_active:
        return

    recipients = MailingRecipient.objects.all()  # или фильтр по нужной группе
    for recipient in recipients:
        try:
            send_mail(
                mailing.title,
                mailing.content,
                os.getenv("EMAIL_HOST_USER"),
                [recipient.email],
            )
            status = "success"
        except Exception:
            status = "failed"
        # Логируем результат
        MessageLog.objects.create(mailing=mailing, recipient=recipient, status=status)
