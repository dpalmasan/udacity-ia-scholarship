import requests
from abc import ABC
import time


class Recognizer:
    def __init__(
        self, ocp_api_key, model="prebuilt-idDocument", key="udacityformrecognizer"
    ):
        self.key = key
        self.ocp_api_key = ocp_api_key
        self.__model = model

    @property
    def endpoint(self):
        return f"https://{self.key}.cognitiveservices.azure.com"

    def analyze(self, image_url: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.ocp_api_key,
        }

        data = {"urlSource": image_url}

        url = (
            f"{self.endpoint}/formrecognizer/documentModels/"
            f"{self.__model}:analyze?api-version=2022-01-30-preview"
        )

        result = requests.post(url, json=data, headers=headers)
        result.raise_for_status()
        return result.headers["Operation-location"]

    def result(self, operation_location: str):
        headers = {
            "Ocp-Apim-Subscription-Key": self.ocp_api_key,
        }
        result = requests.get(operation_location, headers=headers)
        result.raise_for_status()
        result_data = result.json()
        while result_data["status"] != "succeeded":
            time.sleep(1)
            result = requests.get(operation_location, headers=headers)
            result.raise_for_status()
            result_data = result.json()
        return result_data


if __name__ == "__main__":
    resource = (
        "https://dpalmastorage.blob.core.windows.net/udacity-data/ca-dl-diogo.png"
    )
    model = "prebuilt-idDocument"
    import os

    resource = "https://dpalmastorage.blob.core.windows.net/udacity-data/boarding_pass_clynton.pdf"
    model = "boarding_ten_samples"
    recognizer = Recognizer(os.getenv("API_KEY"), model=model)
    operation_location = recognizer.analyze(resource)
    print(recognizer.result(operation_location))