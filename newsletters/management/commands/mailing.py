import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from newsletters.models import MailingAttempt, Newsletter

load_dotenv()


class Command(BaseCommand):
    help = "Запуск рассылки по ID рассылки"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]
        mailing = Newsletter.objects.get(pk=mailing_id)
        recipients = mailing.recipients.all()

        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.title,
                    mailing.message.content,
                    os.getenv("EMAIL_HOST_USER"),
                    [recipient.email],
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="success",
                    server_response="Письмо успешно отправлено",
                )
                self.stdout.write(f"Отправлено {recipient.email}")
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing, status="failure", server_response=str(e)
                )
                self.stderr.write(f"Ошибка при отправке {recipient.email}: {e}")
