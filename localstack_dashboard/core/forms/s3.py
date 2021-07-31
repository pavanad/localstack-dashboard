# -*- coding: utf-8 -*-

from botocore.exceptions import ClientError
from django import forms
from django.core.exceptions import ValidationError
from localstack_dashboard.boto3_wrapper.s3 import (
    bucket_exists,
    bucket_is_valid,
    s3_client,
)
from localstack_dashboard.boto3_wrapper.session import (
    get_available_regions,
    get_current_region_name,
)


class BucketForm(forms.Form):
    name = forms.CharField(
        label="Bucket name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    choices_region = ((region, region) for region in get_available_regions("s3"))
    region = forms.ChoiceField(
        label="AWS Region",
        choices=choices_region,
        widget=forms.Select(attrs={"class": "form-control"}),
        initial=get_current_region_name(),
    )

    def clean_name(self):
        data = self.cleaned_data["name"]
        if not bucket_is_valid(data):
            raise ValidationError("The specified bucket name is not valid")
        if bucket_exists(data):
            raise ValidationError("Bucket name already exists")
        return data

    def create_bucket(self, name: str, region: str) -> bool:
        try:
            s3 = s3_client(region)
            s3.create_bucket(
                Bucket=name, CreateBucketConfiguration={"LocationConstraint": region}
            )
        except ClientError as error:
            print(f"{error}")
            return False
        return True
