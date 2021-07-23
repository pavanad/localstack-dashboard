# -*- coding: utf-8 -*-

from django.urls import path

from .views.dashboard import DashboardView

app_name = "core"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
]
