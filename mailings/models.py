from django.db import models

# class MailingRecipient(models.Model):
#
#     class Meta:
#         managed = True
#         db_table = 'users_mailingrecipient'


class Mailings(models.Model):
    title = models.CharField(max_length=50, verbose_name="Тема письма", help_text="Введите тему письма")
    content = models.TextField(verbose_name="Тело письма", help_text="Введите текст письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title


class MessageLog(models.Model):
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='messages')
    # recipient = models.ForeignKey('users.MailingRecipient', on_delete=models.CASCADE, related_name='messages_sent')
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed')])
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mailing.title} to {self.recipient.email} - {self.status}"
