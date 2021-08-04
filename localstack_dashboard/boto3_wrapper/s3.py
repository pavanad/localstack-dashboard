# -*- coding: utf-8 -*-

import re

import boto3
from localstack_dashboard.config.parser import get_endpoint_url

ENDPOINT = get_endpoint_url()


def s3_resource():
    s3 = boto3.resource("s3", endpoint_url=ENDPOINT)
    return s3


def s3_client(region: str = None):
    s3 = boto3.client("s3", endpoint_url=ENDPOINT)
    if region is not None:
        s3 = boto3.client("s3", endpoint_url=ENDPOINT, region_name=region)
    return s3


def bucket_exists(bucket_name: str) -> bool:
    s3 = s3_resource()
    return s3.Bucket(bucket_name) in s3.buckets.all()


def bucket_is_valid(bucket_name: str) -> bool:
    regex = r"(?=^.{3,63}$)(?!xn--)([a-z0-9](?:[a-z0-9-]*)[a-z0-9])$"
    matches = re.search(regex, bucket_name)
    return matches is not None


def delete_bucket(bucket_name: str):
    s3 = s3_resource()
    bucket = s3.Bucket(bucket_name)
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()
