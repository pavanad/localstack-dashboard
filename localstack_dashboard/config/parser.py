import os
from configparser import ConfigParser
from pathlib import Path

CONFIG_FILENAME = "localstack.conf"
CONFIG_ROOT_PATH = Path(__file__).resolve().parent.parent


def config_file_exists() -> bool:
    filename = os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME)
    return os.path.exists(filename)


def get_configurations() -> ConfigParser:
    if not config_file_exists():
        set_default_configurations()

    configuration = ConfigParser()
    configuration.read(os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME))
    return configuration


def get_configurations_values():
    config = get_configurations()
    section_name = "default"
    if config.has_section("custom"):
        section_name = "custom"

    data = {}
    for key in config[section_name]:
        data[key] = config.get(section_name, key)
    return data


def get_endpoint_url() -> str:
    config = get_configurations()
    port = config.get("default", "edge_port")
    hostname = config.get("default", "hostname")

    if config.has_section("custom"):
        port = config.get("custom", "edge_port")
        hostname = config.get("custom", "hostname")

    return f"http://{hostname}:{port}"


def set_default_configurations():
    configuration = ConfigParser()
    configuration["default"] = {
        "edge_port": "4566",
        "hostname": "localhost",
        "region": "us-east-1",
    }
    set_configurations(configuration)


def set_configurations(configuration: ConfigParser):
    filename = os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME)
    with open(filename, "w") as config_file:
        configuration.write(config_file)
