# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from localstack_dashboard.boto3_wrapper.s3 import s3_client
from localstack_dashboard.core.forms.s3 import BucketForm
from localstack_dashboard.core.mixins.localstack_service_mixin import (
    LocalStackServiceMixin,
)


class S3View(LocalStackServiceMixin, TemplateView):
    template_name = "services/s3.html"
    redirect_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        s3 = s3_client()
        response = s3.list_buckets()

        context.update(
            {
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
    form_class = BucketForm
    template_name = "services/s3_bucket_create_form.html"
    success_url = "/s3/"
    redirect_url = "/"

    def form_valid(self, form):
        name = self.request.POST.get("name")
        region = self.request.POST.get("region")
        form.create_bucket(name, region)
        return super().form_valid(form)
