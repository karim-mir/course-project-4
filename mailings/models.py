import uuid

from django.db import models


class Mailings(models.Model):
    title = models.CharField(max_length=50, verbose_name="Тема письма", help_text="Введите тему письма")
    content = models.TextField(verbose_name="Тело письма", help_text="Введите текст письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title


class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(
        max_length=100, verbose_name="Ф.И.О.", help_text="Введите свое Ф.И.О."
    )
    comment = models.TextField(
        verbose_name="Комментарий", help_text="Введите свой комментарий"
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )


class MessageLog(models.Model):
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='messages')
    recipient = models.ForeignKey(MailingRecipient, on_delete=models.CASCADE, related_name='messages_sent')
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed')])
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mailing.title} to {self.recipient.email} - {self.status}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"
        managed = True

    def __str__(self):
        return self.email


class EmailConfirmation(models.Model):
    """ Моедль для автоматической генерации токена """
    user = models.OneToOneField(MailingRecipient, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email confirmation for {self.user.email}"
