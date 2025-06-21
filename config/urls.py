from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("mailings/", include("mailings.urls", namespace="mailings")),
    path("newsletters/", include("newsletters.urls", namespace="newsletters")),
]
