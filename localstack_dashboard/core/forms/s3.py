# -*- coding: utf-8 -*-

from botocore.exceptions import ClientError
from django import forms
from localstack_dashboard.boto3_wrapper.session import (
    get_available_regions,
    get_current_region_name,
)
from localstack_dashboard.boto3_wrapper.s3 import s3_client


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
