from pathlib import Path
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)


def predict(
    predictor: CustomVisionPredictionClient,
    image_path: Path,
    project_id: str,
    publish_iteration_name: str,
):
    with open(image_path, "rb") as image_contents:
        results = predictor.detect_image(
            project_id, publish_iteration_name, image_contents.read()
        )

    return results
