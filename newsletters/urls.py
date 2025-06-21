from django.urls import path
from newsletters.apps import NewslettersConfig
from newsletters.models import Newsletter

from .views import (
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView,
    NewsletterUpdateView,
    NewsletterDeleteView,
    mailing_statistics,
    manual_send_newsletter,
)

app_name = NewslettersConfig.name
urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletters_list'),
    path('<int:pk>/', NewsletterDetailView.as_view(), name='newsletters_detail'),
    path('add/', NewsletterCreateView.as_view(), name='newsletters_add'),
    path('<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletters_edit'),
    path('<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletters_delete'),
    path('<int:pk>/send/', manual_send_newsletter, name='send_newsletter'),
    path('mailing/<int:pk>/stats/', mailing_statistics, name='mailing_statistics'),
]
