from boto3.session import Session


def get_current_region_name() -> str:
    session = Session()
    return session.region_name


def get_available_regions(service_name: str) -> list:
    session = Session()
    return session.get_available_regions(service_name)
