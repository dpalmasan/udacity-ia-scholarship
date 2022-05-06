import csv
import datetime
import logging
from pathlib import Path
from typing import Dict, List
import uuid

from step_2.form_recognizers import Recognizer
from step_3.video import (
    build_person_group,
    detect_faces,
    get_image_thumbnails,
    save_images,
)
from step_4.lighter_detector import predict
from utils import config
from video_indexer import VideoIndexer
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FORMAT = "%(asctime)s %(module)s  %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


ID_PATH = Path("/mnt/c/Users/dpalma/Desktop/ids")
BLOB_STORAGE_URL = "https://dpalmastorage.blob.core.windows.net/udacity-data"
MANIFEST_ROOT = Path("manifest_table")

MANIFEST_MAPPINGS = {
    "FirstName": "First Name",
    "Last Name": "Last Name",
    "Sex": "Sex",
    "DateOfBirth": "DateOfBirth",
    "flightNumber": "Flight No",
    "origin": "Origin",
    "destination": "Destination",
    "date": "Date",
    "lastName": "Last Name",
    "firstName": "First Name",
    "seatNumber": "SeatNo",
    "time": "Time",
}


class Validation:
    def __init__(self, id_info, bp_info, manifest_data):
        self.id_info = dict(id_info)
        self.bp_info = dict(bp_info)
        self.manifest_data = {
            key: dict(data) for key, data in manifest_data.items()
        }

    def validate_text_data(self, passenger):
        # Considering that in some cases a person might have two names
        # In the ID
        name_validation = (
            self.manifest_data[passenger]["First Name"].split()[0]
            == self.bp_info["First Name"].split()[0]
            == self.id_info["First Name"].split()[0]
        )

        if name_validation:
            self.manifest_data[passenger]["NameValidation"] = "TRUE"

        dob_validation = self.id_info["DateOfBirth"] == canonicalize_dob(
            self.manifest_data[passenger]["DateOfBirth"]
        )
        if dob_validation:
            self.manifest_data[passenger]["DoBValidation"] = "TRUE"

        bp_validation = (
            self.manifest_data[passenger]["Flight No"]
            == self.bp_info["Flight No"]
            and self.manifest_data[passenger]["Origin"]
            == self.bp_info["Origin"]
            and self.manifest_data[passenger]["Destination"]
            == self.bp_info["Destination"]
            and self.bp_info["Date"] == self.manifest_data[passenger]["Date"]
            and self.bp_info["Time"] == self.manifest_data[passenger]["Time"]
            and self.bp_info["Time"] == self.manifest_data[passenger]["Time"]
            and self.bp_info["SeatNo"]
            == self.manifest_data[passenger]["SeatNo"]
        )

        if bp_validation:
            self.manifest_data[passenger]["BoardingPassValidation"] = "TRUE"


def canonicalize_dob(date_str: str) -> str:
    """Convert d MonthName YYYY format to YYYY-M-D

    Data in the boarding pass is in 12-hour clock (did on purpose for fun), and
    data in the manifest is in 24-hour clock. This function does the conversion
    so we can compare with the manifest data.

    :param date_str: Value of the field
    :type value: str
    :return: Canonicalized date str
    :rtype: str
    """
    return datetime.datetime.strptime(date_str, "%d %B %Y").strftime(
        "%Y-%m-%d"
    )


def process_boarding_value(field: str, value: str) -> str:
    """Convert from 12-hour clock to 24-hour clock.

    Data in the boarding pass is in 12-hour clock (did on purpose for fun), and
    data in the manifest is in 24-hour clock. This function does the conversion
    so we can compare with the manifest data.

    :param field: Only convert if field is ``Time``
    :type field: str
    :param value: Value of the field
    :type value: str
    :return: Just the field value if it is not Time, converted otherwise
    :rtype: str
    """
    if field == "Time":
        return datetime.datetime.strptime(value, "%I:%M %p").strftime("%H:%M")
    return value


def load_manifest_data(
    manifest_path: Path, passenger_order: List[str]
) -> Dict[str, str]:
    result = {}
    with open(manifest_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row, passenger in zip(reader, passenger_order):
            result[passenger] = row

    return result


def write_manifest_data(
    manifest_path: Path, passenger_order: List[str], data: Dict[str, str]
):
    with open(manifest_path, "w") as csvfile:
        fieldnames = [
            "Flight No",
            "Origin",
            "Destination",
            "Date",
            "Time",
            "First Name",
            "Last Name",
            "Sex",
            "SeatNo",
            "DateOfBirth",
            "DoBValidation",
            "PersonValidation",
            "LuggageValidation",
            "NameValidation",
            "BoardingPassValidation",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for passenger in passenger_order:
            writer.writerow(data[passenger])


def step_2(
    id_doc_model: Recognizer,
    boarding_pass_model: Recognizer,
    person_id_doc: str,
    person_boarding_pass: str,
):
    resource = f"{BLOB_STORAGE_URL}/{person_id_doc}"
    op_location = id_doc_model.analyze(resource)
    id_info = id_doc_model.result(op_location)
    id_relevant_info = {}
    for field, value in id_info["analyzeResult"]["documents"][0][
        "fields"
    ].items():
        if field in MANIFEST_MAPPINGS:
            id_relevant_info[MANIFEST_MAPPINGS[field]] = (
                value["valueDate"]
                if value["type"] == "date"
                else value["valueString"]
            )
    resource = f"{BLOB_STORAGE_URL}/{person_boarding_pass}"
    op_location = boarding_pass_model.analyze(resource)
    boarding_pass_info = boarding_pass_model.result(op_location)
    boarding_pass_relevant_info = {}
    for field, value in boarding_pass_info["analyzeResult"]["documents"][0][
        "fields"
    ].items():
        if field in MANIFEST_MAPPINGS:
            field = MANIFEST_MAPPINGS[field]
            boarding_pass_relevant_info[field] = (
                value["valueDate"]
                if value["type"] == "date"
                else process_boarding_value(field, value["valueString"])
            )

    return id_relevant_info, boarding_pass_relevant_info


def step_3():
    video_id = "89fe0aeb73"
    indexer = VideoIndexer(
        vi_subscription_key=config.vi_subscription_key,
        vi_location="trial",
        vi_account_id=config.vi_account_id,
    )
    images, info = get_image_thumbnails(indexer, video_id)
    save_images(ID_PATH, images)

    service_endpoint = config.face_service_endpoint
    service_key = config.face_service_key
    face_client = FaceClient(
        service_endpoint, CognitiveServicesCredentials(service_key)
    )

    PERSON_GROUP_ID = str(uuid.uuid4())
    person_group_name = "person-dpalma"
    build_person_group(
        face_client, PERSON_GROUP_ID, person_group_name, ID_PATH
    )
    logger.info(info["summarizedInsights"]["sentiments"])
    logger.info(info["summarizedInsights"]["emotions"])

    video_ids = detect_faces(face_client, ID_PATH.glob("human-face*.jpg"))
    dl_ids = {}
    for image_path in ID_PATH.glob("ca-dl*.png"):
        with open(image_path, "rb") as img:
            dl_faces = face_client.face.detect_with_stream(img)

        for face in dl_faces:
            dl_ids[image_path.stem] = face.face_id

    logger.info(dl_ids)

    for name, dl_id in dl_ids.items():
        dl_verify_result = face_client.face.verify_face_to_face(
            video_ids["human-face4"], dl_id
        )
        logger.info(f"Comparing human-face4 to {name}")
        if dl_verify_result.is_identical:
            logger.info(
                "Faces are of the same (Positive) person, "
                f"similarity confidence: {dl_verify_result.confidence}."
            )
        else:
            logger.info(
                "Faces are of different (Negative) persons, "
                f"similarity confidence: {dl_verify_result.confidence}."
            )


def step_4():
    prediction_credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": config.prediction_key}
    )
    predictor = CustomVisionPredictionClient(
        config.endpoint, prediction_credentials
    )
    image_dir = ID_PATH / "lighter_test_images"

    for image_path in image_dir.glob("*.jpg"):
        results = predict(
            predictor,
            image_path,
            config.project_id,
            config.publish_iteration_name,
        )

        logger.info(results.predictions)
        with open(image_path, "rb") as img_code:
            img_view_ready = Image.open(img_code)
            _, ax = plt.subplots()
            ax.imshow(img_view_ready)
            for prediction in results.predictions:
                logger.info(
                    f"{prediction.tag_name}"
                    ": {0:.2f}%".format(prediction.probability * 100)
                )
                if prediction.probability > 0.8:
                    bbox = prediction.bounding_box
                    rect = patches.Rectangle(
                        (
                            bbox.left * img_view_ready.width,
                            (1 - bbox.top) * img_view_ready.height,
                        ),
                        bbox.width * img_view_ready.width,
                        -bbox.height * img_view_ready.height,
                        linewidth=1,
                        edgecolor="r",
                        facecolor="none",
                    )
                    ax.add_patch(rect)
    plt.show()


def main():
    # id_doc_model = Recognizer(
    #    config.form_recognizer_api_key, model="prebuilt-idDocument"
    # )
    # boarding_pass_model = Recognizer(
    #    config.form_recognizer_api_key, model="boarding_ten_samples"
    # )
    #
    # person_id_doc = "ca-dl-diogo.png"
    # person_boarding_pass = "boarding_pass_diogo.pdf"
    # id_info, bp_info = step_2(
    #    id_doc_model, boarding_pass_model, person_id_doc, person_boarding_pass
    # )
    # logger.info(id_info)
    # logger.info(bp_info)
    # id_info = {
    #     "DateOfBirth": "1990-01-17",
    #     "First Name": "Diogo Andrés",
    #     "Sex": "M",
    # }
    # bp_info = {
    #     "First Name": "Diogo",
    #     "Origin": "Santiago",
    #     "Destination": "Concepción",
    #     "Time": "11:00",
    #     "Flight No": "LA-21",
    #     "Last Name": "Puelma",
    #     "SeatNo": "3A",
    #     "Date": "10 April 2022",
    # }
    # passenger_order = ["diogo", "manuel", "clynton", "norma", "javiera"]
    # input_manifest_path = MANIFEST_ROOT / "manifest.csv"
    # output_manifest_path = MANIFEST_ROOT / "manifest_validated.csv"
    # manifest_data = load_manifest_data(input_manifest_path, passenger_order)
    # validation = Validation(id_info, bp_info, manifest_data)
    # validation.validate_text_data("diogo")
    # write_manifest_data(
    #     output_manifest_path, passenger_order, validation.manifest_data
    # )
    pass


if __name__ == "__main__":
    main()
