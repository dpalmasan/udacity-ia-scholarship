import logging
import yaml
from dataclasses import dataclass

_LOG_LEVEL_MAPPING = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


def get_log_level(level: str) -> str:
    try:
        return _LOG_LEVEL_MAPPING[level]
    except KeyError:
        raise KeyError(
            f"Invalid log level, choose one of {_LOG_LEVEL_MAPPING.keys()}"
        )


@dataclass
class Config:
    form_recognizer_api_key: str
    api_key: str
    vi_account_id: str
    vi_subscription_key: str
    face_service_endpoint: str
    face_service_key: str
    endpoint: str
    prediction_key: str
    project_id: str
    publish_iteration_name: str
    log_level: str
    is_free_tier: bool
    show_lighter_detection: bool


with open("config.yaml", "r") as fp:
    config_params = yaml.load(fp, yaml.SafeLoader)

config = Config(**config_params)
