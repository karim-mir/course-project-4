from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from . import views
#from .views import (MailingRecipientCreateView, MailingRecipientDeleteView,
 #                   MailingRecipientDetailView, MailingRecipientListView,
 #                   MailingRecipientUpdateView, confirm_email)
app_name = UsersConfig.name
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    #Получатели рассылки
    #path("recipients/", MailingRecipientListView.as_view(), name="recipients_list"),
    #path(
    #    "recipients/<int:pk>/",
    #    MailingRecipientDetailView.as_view(),
    #    name="recipient_detail",
    #),
    #path("recipients/add/", MailingRecipientCreateView.as_view(), name="recipient_add"),
    #path(
    #    "recipients/<int:pk>/edit/",
    #    MailingRecipientUpdateView.as_view(),
    #    name="recipient_edit",
    #),
    #path(
    #    "recipients/<int:pk>/delete/",
    #    MailingRecipientDeleteView.as_view(),
    #    name="recipient_delete",
    #),
    ## подтверждение email
    #path("confirm/<uuid:token>/", confirm_email, name="confirm_email"),
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
]
