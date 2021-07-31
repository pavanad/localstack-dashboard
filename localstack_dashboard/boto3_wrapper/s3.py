import boto3
from localstack_dashboard.config.parser import get_endpoint_url

ENDPOINT = get_endpoint_url()


def s3_client(region: str = None):
    s3 = boto3.client("s3", endpoint_url=ENDPOINT)
    if region is not None:
        s3 = boto3.client("s3", endpoint_url=ENDPOINT, region_name=region)
    return s3
