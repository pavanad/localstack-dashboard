# -*- coding: utf-8 -*-

from django.urls import path
from localstack_dashboard.core.views import dashboard, s3, settings

app_name = "core"

urlpatterns = [
    path("", dashboard.DashboardView.as_view(), name="index"),
    path("settings/", settings.SettingsView.as_view(), name="settings"),
    path("s3/", s3.S3View.as_view(), name="s3"),
    path("s3/bucket/create", s3.BucketCreateView.as_view(), name="s3_bucket_create"),
    path("s3/bucket/<name>/delete", s3.BucketDeleteView.as_view(), name="s3_bucket_delete")
]
