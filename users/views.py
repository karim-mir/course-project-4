from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.db.models import Count, Q

from mailings.models import MailingRecipient

from users.forms import CustomUserRegistrationForm, MailingRecipientForm
from users.models import EmailConfirmation



## Получение статистики по пользователю
#recipients_stats = MailingRecipient.objects.annotate(
#    total_messages=Count("messages_sent"),
#    success_count=Count("messages_sent", filter=Q(messages_sent__status="success")),
#    failed_count=Count("messages_sent", filter=Q(messages_sent__status="failed"))
#)
#
#for recipient in recipients_stats:
#    print(f"{recipient.email}:")
#    print(f"  Всего сообщений: {recipient.total_messages}")
#    print(f"  Успешных: {recipient.success_count}")
#    print(f"  Неудачных: {recipient.failed_count}")


def confirm_email(request, token):
    """Функция для обработки ссылки подтверждения"""
    try:
        confirmation = EmailConfirmation.objects.get(token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return render(request, "users/confirmation_success.html")
    except EmailConfirmation.DoesNotExist:
        return render(request, "users/confirmation_invalid.html")


def register(request):
    """Функция для регистрации, создагния токена и отправки письма"""
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # отключаем до подтверждения email
            user.save()

            # Создаем токен подтверждения
            confirmation = EmailConfirmation.objects.create(user=user)

            # Отправляем письмо с ссылкой на подтверждение
            confirm_url = request.build_absolute_uri(
                reverse("confirm_email", args=[str(confirmation.token)])
            )
            send_mail(
                "Подтверждение регистрации",
                f"Перейдите по ссылке для подтверждения: {confirm_url}",
                "your_email@example.com",
                [user.email],
            )

            return render(
                request, "users/registration_pending.html"
            )  # страница с инструкциями
    else:
        form = CustomUserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("users:home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("users:login")


def home(request):
    return render(request, "users/home.html")


class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = "users/recipients_list.html"
    context_object_name = "users"


class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = "users/recipients_detail.html"

    def get_queryset(self):
        return get_users_from_cache()


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    template_name = "users/recipients_form.html"
    form_class = MailingRecipientForm


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    template_name = "users/recipients_form.html"
    form_class = MailingRecipientForm
    success_url = reverse_lazy("users:recipients_list")


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = "users/recipients_confirm_delete.html"
    success_url = reverse_lazy("users:recipients_list")
