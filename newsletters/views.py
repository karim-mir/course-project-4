from dotenv import load_dotenv

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newsletters.models import Newsletter, MailingAttempt
from .services.send_newsletter_email import send_newsletter_email  # импорт функции отправки

import os

load_dotenv()

def mailing_statistics(request, pk):
    """ Функция статистики и отчетности по попыткам рассылок """
    mailing = get_object_or_404(Newsletter, pk=pk)
    attempts = MailingAttempt.objects.filter(mailing=mailing)

    total_attempts = attempts.count()
    success_count = attempts.filter(status='success').count()
    failure_count = attempts.filter(status='failure').count()

    context = {
        'mailing': mailing,
        'total_attempts': total_attempts,
        'success_count': success_count,
        'failure_count': failure_count,
        'attempts': attempts,
    }

    return render(request, 'newsletters/mailing_statistics.html', context)

def notify_admin_about_status(success_count, failure_count):
    """ Вспомогательная функция для уведомления по почте о результате рассылки """
    subject = "Отчет о рассылке"
    message = f"Рассылка завершена.\nУспешных отправлений: {success_count}\nОшибок: {failure_count}"
    from_email = os.getenv('EMAIL_HOST_USER')
    recipient_list = ['your_email@example.com']
    send_mail(subject, message, from_email, recipient_list)


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "newsletters/newsletters_list.html"
    context_object_name = "newsletters"


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = "newsletters/newsletters_detail.html"


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    template_name = "newsletters/newsletters_form.html"
    fields = ["start_datetime", "end_datetime", "status", "message", "recipient"]
    success_url = reverse_lazy("newsletters:newsletters_list")


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    template_name = "newsletters/newsletters_form.html"
    fields = ["start_datetime", "end_datetime", "status", "message", "recipient"]
    success_url = reverse_lazy("newsletters:newsletters_list")


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    template_name = "newsletters/newsletters_confirm_delete.html"
    success_url = reverse_lazy("newsletters:newsletters_list")


def manual_send_newsletter(request, pk):
    mailing = get_object_or_404(Newsletter, pk=pk)

    recipients = mailing.recipient.all()

    success_count = 0
    failure_count = 0

    for recipient in recipients:
        result = send_newsletter_email(mailing, recipient.email)
        if result:
            success_count += 1
        else:
            failure_count += 1

    # Отправляем отчет на почту администратора или себя
    notify_admin_about_status(success_count, failure_count)

    messages.success(request, "Рассылка запущена.")
    return redirect('newsletters:newsletters_detail', pk=pk)
