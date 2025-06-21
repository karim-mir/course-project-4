from django.db import models
from django.utils import timezone
from mailings.models import Mailing, MailingRecipient

NEWSLETTERS_STATUS_CHOICES = [
    ("Создана", "Создана"),
    ("Запущена", "Запущена"),
    ("Завершена", "Завершена"),
]

class Newsletter(models.Model):
    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки",
                                help_text="Введите дату и время первой отправки")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания отправки",
                                help_text="Введите дату и время окончания отправки")
    status = models.CharField(
        max_length=10,
        choices=NEWSLETTERS_STATUS_CHOICES,
        default="Создана",
        verbose_name="Статус",
        help_text="Выберите статус рассылки"
    )
    message = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(MailingRecipient)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return (f"Статус:{self.status}, сообщение:{self.message.title}")


class MailingAttempt(models.Model):
    STATUS_CHOICES_MAILINGS = [
        ("success", "Успешно"),
        ("failure", "Не успешно"),
    ]

    mailing = models.ForeignKey("Newsletter", on_delete=models.CASCADE, related_name="attempts")
    attempt_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES_MAILINGS)
    server_response = models.TextField(blank=True)

    def __str__(self):
        return f"Попытка {self.mailing} на {self.attempt_time} - {self.get_status_display()}"


class Letter(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.name
