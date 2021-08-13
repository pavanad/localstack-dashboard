# -*- coding: utf-8 -*-

import os

from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from localstack_dashboard.boto3_wrapper.s3 import delete_bucket, s3_client
from localstack_dashboard.core.forms.s3 import BucketForm
from localstack_dashboard.core.mixins.localstack_service_mixin import (
    LocalStackServiceMixin,
)


class S3View(LocalStackServiceMixin, TemplateView):
    redirect_url = "/"
    template_name = "services/s3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        s3 = s3_client()
        response = s3.list_buckets()

        description = "Buckets are containers for data stored in S3. \
                      <a href='https://docs.aws.amazon.com/console/s3/storage_lens' target='_blank'>Learn more</a>"

        context.update(
            {
                "type": "buckets",
                "title": "Buckets",
                "description": description,
                "empty_message": "<strong>No bucket</strong> - You don’t have any buckets.",
                "bucket_list": [
                    {
                        "Name": item["Name"],
                        "Region": "",
                        "Access": "Bucket and objects not public",
                        "CreationDate": item["CreationDate"],
                    }
                    for item in response["Buckets"]
                ],
            }
        )
        return context


class BucketCreateView(LocalStackServiceMixin, FormView):
    redirect_url = "/"
    success_url = "/s3/"
    form_class = BucketForm
    template_name = "services/s3_bucket_create_form.html"

    def form_valid(self, form):
        name = self.request.POST.get("name")
        region = self.request.POST.get("region")
        form.create_bucket(name, region)
        return super().form_valid(form)


class BucketCreateView(LocalStackServiceMixin, FormView):
    redirect_url = "/"
    success_url = "/s3/"
    form_class = BucketForm
    template_name = "services/s3_bucket_create_form.html"

    def form_valid(self, form):
        name = self.request.POST.get("name")
        region = self.request.POST.get("region")
        form.create_bucket(name, region)
        return super().form_valid(form)


class BucketDeleteView(LocalStackServiceMixin, TemplateView):
    redirect_url = "/"
    template_name = "services/s3_bucket_delete_confirm.html"

    def post(self, request, *args, **kwargs):
        self.bucket_name = kwargs.get("name")
        if request.POST.get("bucket_name") == self.bucket_name:
            delete_bucket(self.bucket_name)
            return redirect("/s3/")
        return render(
            request,
            self.template_name,
            {"bucket_name": self.bucket_name, "error": "Bucket doesn't check"},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.bucket_name = kwargs.get("name")
        context["bucket_name"] = self.bucket_name
        return context


class BucketShowView(LocalStackServiceMixin, TemplateView):
    redirect_url = "/"
    template_name = "services/s3.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket_name = kwargs.get("name")

        s3 = s3_client()
        response = s3.list_objects_v2(Bucket=bucket_name)

        object_list = []
        for item in response["Contents"]:
            key_type = os.path.splitext(item["Key"])[1].replace(".", "")
            item.update({"Type": key_type})
            object_list.append(item)

        context.update(
            {
                "type": "objects",
                "title": "Objects",
                "description": "Objects are the fundamental entities stored in Amazon S3.",
                "empty_message": "<strong>No objects</strong> - You don't have any objects in this bucket.",
                "object_list": object_list,
            }
        )
        return context
