import yaml
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str
    vi_account_id: str
    vi_subscription_key: str
    face_service_endpoint: str
    face_service_key: str


with open("config.yaml", "r") as fp:
    config_params = yaml.load(fp, yaml.SafeLoader)

config = Config(**config_params)
