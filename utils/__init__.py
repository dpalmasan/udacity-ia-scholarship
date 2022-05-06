import yaml
from dataclasses import dataclass


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


with open("config.yaml", "r") as fp:
    config_params = yaml.load(fp, yaml.SafeLoader)

config = Config(**config_params)
