from django.conf import settings
from django.db import models

from django.urls import reverse
import uuid


class Mailing(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=50, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    content = models.TextField(
        verbose_name="Тело письма", help_text="Введите текст письма"
    )
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('mailings:mailings_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_disable_mailing", "Может отключать рассылки"),
        ]

    def __str__(self):
        return self.title


class MailingRecipient(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.", help_text="Введите свое Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", help_text="Введите свой комментарий")
    token = models.CharField(max_length=100, blank=True, null=True, default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse('mailings:recipients_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"


class MessageLog(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="messages"
    )
    recipient = models.ForeignKey(
        MailingRecipient, on_delete=models.CASCADE, related_name="messages_sent"
    )
    status = models.CharField(
        max_length=10, choices=[("success", "Success"), ("failed", "Failed")]
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mailing.title} to {self.recipient.email} - {self.status}"

    class Meta:
        verbose_name = "Журнал сообщений"
        verbose_name_plural = "Журналы сообщений"
        managed = True
