from django.urls import path

from mailings.apps import MailingsConfig

from . import views
from .views import (MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView)

app_name = MailingsConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailings_list"),
    path("<int:pk>/", MailingDetailView.as_view(), name="mailings_detail"),
    path("add/", MailingCreateView.as_view(), name="mailings_add"),
    path("<int:pk>/edit/", MailingUpdateView.as_view(), name="mailings_edit"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailings_delete"),
    path("send/<int:pk>/", views.start_mailing, name="start_mailing"),
    path("<int:pk>/disable/", views.disable_mailing, name="disable_mailing"),
]
