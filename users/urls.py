from django.contrib.auth import views as auth_views

from django.urls import path, reverse_lazy

from users.apps import UsersConfig

from . import views
from .views import (
    confirm_email,
)

app_name = UsersConfig.name
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.user_profile, name="profile"),
    path("registration_pending/", views.registration_pending, name="registration_pending"),
    # подтверждение email
    path("confirm/<uuid:token>/", confirm_email, name="confirm_email"),
    # восстановление пароля
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Форма запроса сброса пароля (ввод email)
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    # Страница с сообщением, что письмо отправлено
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # Ссылка из письма — форма для ввода нового пароля
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # Страница успешного сброса пароля
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
