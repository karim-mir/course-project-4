import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class MailingRecipient(AbstractUser):
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

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
