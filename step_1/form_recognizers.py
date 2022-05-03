import requests
from abc import ABC
import time


class Recognizer(ABC):
    key = ""

    @property
    def endpoint(self):
        return f"https://{self.key}.cognitiveservices.azure.com"


class IdentificationRecognizer(Recognizer):
    __model = "prebuilt-idDocument"

    def __init__(self, ocp_api_key, key="udacityformrecognizer"):
        self.key = key
        self.ocp_api_key = ocp_api_key

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
    image_url = (
        "https://dpalmastorage.blob.core.windows.net/udacity-data/ca-dl-diogo.png"
    )
    # image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png"
    import os

    recognizer = IdentificationRecognizer(os.getenv("API_KEY"))
    operation_location = recognizer.analyze(image_url)
    print(recognizer.result(operation_location))
