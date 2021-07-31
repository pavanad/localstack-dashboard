"""localstack_dashboard URL Configuration"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("localstack_dashboard.core.urls", namespace="core")),
]
