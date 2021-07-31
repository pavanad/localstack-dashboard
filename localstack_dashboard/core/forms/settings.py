# -*- coding: utf-8 -*-

from django import forms
from localstack_dashboard.boto3_wrapper.session import (
    get_available_regions,
    get_current_region_name,
)
from localstack_dashboard.config.parser import get_configurations, set_configurations


class SettingsForm(forms.Form):
    hostname = forms.CharField(
        label="Hostname",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    edge_port = forms.CharField(
        label="Edge Port",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choices_region = ((region, region) for region in get_available_regions("s3"))
    region = forms.ChoiceField(
        label="Default Region",
        choices=choices_region,
        widget=forms.Select(attrs={"class": "form-control"}),
        initial=get_current_region_name(),
    )

    def save_configurations(self, hostname: str, port: str, region: str):
        configuration = get_configurations()
        configuration["custom"] = {
            "edge_port": port,
            "hostname": hostname,
            "region": region,
        }
        set_configurations(configuration)
