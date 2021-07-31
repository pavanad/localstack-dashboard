# -*- coding: utf-8 -*-

import requests
from localstack_dashboard.config.parser import get_endpoint_url


def localstack_service(request) -> dict:
    """Return localstack service status"""

    try:
        data = {}
        endpoint_url = get_endpoint_url()
        response = requests.get(f"{endpoint_url}/health?reload")
        data["localstack"] = response.json()
        data["localstack"].update(
            {
                "status_code": response.status_code,
                "status_message": "running",
                "status_color": "success",
            }
        )
    except Exception as error:
        print(f"{error}")
        data["localstack"] = {
            "status_code": "503",
            "status_message": "unavailable",
            "status_color": "danger",
        }

    return data
