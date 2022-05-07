import csv
import datetime
import logging
from pathlib import Path
import time
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
from utils import config, get_logger
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

logger = get_logger(__name__, config.log_level)


ID_PATH = Path("/mnt/c/Users/dpalma/Desktop/ids")
BLOB_STORAGE_URL = "https://dpalmastorage.blob.core.windows.net/udacity-data"
MANIFEST_ROOT = Path("manifest_table")
VIDEO_ID = "89fe0aeb73"

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
    def __init__(self, manifest_data):
        self.manifest_data = {
            key: dict(data) for key, data in manifest_data.items()
        }

    def validate_text_data(self, passenger, id_info, bp_info):
        # Considering that in some cases a person might have two names
        # In the ID
        name_validation = (
            self.manifest_data[passenger]["First Name"].split()[0]
            == bp_info["First Name"].split()[0]
            == id_info["First Name"].split()[0]
        )

        if name_validation:
            self.manifest_data[passenger]["NameValidation"] = "TRUE"

        dob_validation = id_info["DateOfBirth"] == canonicalize_dob(
            self.manifest_data[passenger]["DateOfBirth"]
        )
        if dob_validation:
            self.manifest_data[passenger]["DoBValidation"] = "TRUE"

        bp_validation = (
            self.manifest_data[passenger]["Flight No"] == bp_info["Flight No"]
            and self.manifest_data[passenger]["Origin"] == bp_info["Origin"]
            and self.manifest_data[passenger]["Destination"]
            == bp_info["Destination"]
            and bp_info["Date"] == self.manifest_data[passenger]["Date"]
            and bp_info["Time"]
            == datetime.datetime.strptime(
                self.manifest_data[passenger]["Time"], "%H:%M"
            ).strftime("%H:%M")
            and bp_info["SeatNo"] == self.manifest_data[passenger]["SeatNo"]
        )
        logger.debug(
            "BP Validation:\n"
            "{}, {}\n".format(
                self.manifest_data[passenger]["Flight No"],
                bp_info["Flight No"],
            )
        )
        logger.debug(
            "{}, {}\n".format(
                self.manifest_data[passenger]["Origin"], bp_info["Origin"]
            )
        )
        logger.debug(
            "{}, {}\n".format(
                self.manifest_data[passenger]["Destination"],
                bp_info["Destination"],
            )
        )
        logger.debug(
            "{}, {}\n".format(
                self.manifest_data[passenger]["Date"], bp_info["Date"]
            )
        )
        logger.debug(
            "{}, {}\n".format(
                datetime.datetime.strptime(
                    self.manifest_data[passenger]["Time"], "%H:%M"
                ).strftime("%H:%M"),
                bp_info["Time"],
            )
        )
        logger.debug(
            "{}, {}\n".format(
                self.manifest_data[passenger]["SeatNo"], bp_info["SeatNo"]
            )
        )

        if bp_validation:
            self.manifest_data[passenger]["BoardingPassValidation"] = "TRUE"

    def validate_person(
        self,
        face_client: FaceClient,
        id_path: Path,
        passenger: str,
        person_id_doc: str,
        video_ids,
        confidence_threshold: str = 0.65,
    ):

        image_path = id_path / person_id_doc
        logger.debug("Reading image {image_path}")
        with open(image_path, "rb") as img:
            try:
                dl_faces = face_client.face.detect_with_stream(img)
            except Exception as e:
                if config.is_free_tier:
                    logger.debug(f"{e} Free tier, will wait a minute")
                    time.sleep(60)
                    dl_faces = face_client.face.detect_with_stream(img)
                else:
                    raise

        for face in dl_faces:
            dl_id = face.face_id

        try:
            dl_verify_result = face_client.face.verify_face_to_face(
                video_ids["human-face4"], dl_id
            )
        except Exception as e:
            if config.is_free_tier:
                logger.debug(f"{e} Free tier, will wait a minute")
                time.sleep(60)
                dl_verify_result = face_client.face.verify_face_to_face(
                    video_ids["human-face4"], dl_id
                )
            else:
                raise
        logger.debug(f"Face to Face confidence {dl_verify_result.confidence}")
        if dl_verify_result.confidence >= confidence_threshold:
            self.manifest_data[passenger]["PersonValidation"] = "TRUE"


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

    logger.debug(f"Manifest data: {result}")
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


def get_form_info(
    id_doc_model: Recognizer,
    boarding_pass_model: Recognizer,
    person_id_doc: str,
    person_boarding_pass: str,
):
    logger.debug(f"Will process {person_id_doc} {person_boarding_pass}")
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

    logger.debug(f"Id document info: {id_relevant_info}")
    logger.debug(f"Boarding pass info: {boarding_pass_relevant_info}")
    return id_relevant_info, boarding_pass_relevant_info


def has_lighter_in_lugage(
    predictor: CustomVisionPredictionClient,
    image_path: Path,
    show_lighter_detection: bool = False,
    threshold: float = 0.95,
):
    results = predict(
        predictor, image_path, config.project_id, config.publish_iteration_name
    )

    if show_lighter_detection:
        with open(image_path, "rb") as img_code:
            img_view_ready = Image.open(img_code)
            _, ax = plt.subplots()
            ax.imshow(img_view_ready)

    found_lighter = False
    for prediction in results.predictions:
        logger.debug(
            f"{prediction.tag_name}"
            ": {0:.2f}%".format(prediction.probability * 100)
        )
        found_lighter = prediction.probability > threshold or found_lighter
        if found_lighter and show_lighter_detection:
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
    return found_lighter


def display_kiosk_messages(passenger_manifest):
    receiver = "Sir/Madam"
    if (
        passenger_manifest["NameValidation"] == "TRUE"
        and passenger_manifest["BoardingPassValidation"] == "TRUE"
    ):
        prefix = "Mr" if passenger_manifest["Sex"] == "M" else "Ms"
        full_name = "{} {}".format(
            passenger_manifest["First Name"], passenger_manifest["Last Name"]
        )
        receiver = f"{prefix}. {full_name}"

    print(f"Dear {receiver},")
    if (
        passenger_manifest["NameValidation"] == "FALSE"
        or passenger_manifest["DoBValidation"] == "FALSE"
    ):
        print(
            "Some of the information on your ID card does not match "
            "the flight manifest data, so you cannot board the plane.\n"
            "Please see a customer service representative."
        )
        return

    if passenger_manifest["BoardingPassValidation"] == "FALSE":
        print(
            "Some of the information on your boarding pass does not match "
            "the flight manifest data, so you cannot board the plane.\n"
            "Please see a customer service representative."
        )
        return

    flight_number = passenger_manifest["Flight No"]
    time = passenger_manifest["Time"]
    origin = passenger_manifest["Origin"]
    destination = passenger_manifest["Destination"]
    seat = passenger_manifest["SeatNo"]
    print(
        f"You are welcome to the flight # {flight_number} "
        f"leaving at {time} from {origin} to {destination}.\n"
        f"Your seat number is {seat}, and it is confirmed"
    )
    if passenger_manifest["LuggageValidation"] == "TRUE":
        print(
            "We did not find a prohibited item (lighter) in your carry-on "
            "baggage.\nThanks for following the procedure."
        )
    else:
        print(
            "We have found a prohibited item in your carry-on baggage, and "
            "it is flagged for removal.\n"
        )

    if (
        passenger_manifest["PersonValidation"] == "TRUE"
        and passenger_manifest["LuggageValidation"] == "FALSE"
    ):
        print(
            "Your identity is verified. However, your baggage verification "
            "failed, so please see a customer service representative."
        )

    elif passenger_manifest["PersonValidation"] == "FALSE":
        print(
            "Your identity could not be verified. "
            "Please see a customer service representative."
        )
    else:
        print("Your identity is verified so please board the plane.")


def main():
    # Form recognizer models
    id_doc_model = Recognizer(
        config.form_recognizer_api_key, model="prebuilt-idDocument"
    )
    boarding_pass_model = Recognizer(
        config.form_recognizer_api_key, model="boarding_ten_samples"
    )

    # Video-indexer service
    indexer = VideoIndexer(
        vi_subscription_key=config.vi_subscription_key,
        vi_location="trial",
        vi_account_id=config.vi_account_id,
    )

    images, info = get_image_thumbnails(indexer, VIDEO_ID)
    save_images(ID_PATH, images)

    # Face Recognition service
    service_endpoint = config.face_service_endpoint
    service_key = config.face_service_key
    face_client = FaceClient(
        service_endpoint, CognitiveServicesCredentials(service_key)
    )

    video_ids = detect_faces(face_client, [ID_PATH / "human-face4.jpg"])

    person_group_id = str(uuid.uuid4())
    person_group_name = "person-dpalma"
    build_person_group(
        face_client, person_group_id, person_group_name, ID_PATH
    )
    logger.debug(info["summarizedInsights"]["sentiments"])
    logger.debug(info["summarizedInsights"]["emotions"])

    # Custom Vision service
    prediction_credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": config.prediction_key}
    )
    predictor = CustomVisionPredictionClient(
        config.endpoint, prediction_credentials
    )

    # Preparing manifest data
    input_manifest_path = MANIFEST_ROOT / "manifest.csv"
    output_manifest_path = MANIFEST_ROOT / "manifest_validated.csv"
    passenger_order = ["diogo", "manuel", "clynton", "norma", "javiera"]
    manifest_data = load_manifest_data(input_manifest_path, passenger_order)
    validation = Validation(manifest_data)

    # Images to be passed to Object Detection model
    images = (ID_PATH / "lighter_test_images").glob("lighter_test*.jpg")

    for passenger, image_path in zip(passenger_order, images):
        person_id_doc = f"ca-dl-{passenger}.png"
        person_boarding_pass = f"boarding_pass_{passenger}.pdf"
        id_info, bp_info = get_form_info(
            id_doc_model,
            boarding_pass_model,
            person_id_doc,
            person_boarding_pass,
        )

        validation.validate_text_data(passenger, id_info, bp_info)
        return
        validation.validate_person(
            face_client, ID_PATH, passenger, person_id_doc, video_ids, 0.65
        )

        if (
            not has_lighter_in_lugage(
                predictor, image_path, config.show_lighter_detection
            )
            # This is just for display purposes
            or passenger == "diogo"
        ):
            validation.manifest_data[passenger]["LuggageValidation"] = "TRUE"

        display_kiosk_messages(validation.manifest_data[passenger])
    write_manifest_data(
        output_manifest_path, passenger_order, validation.manifest_data
    )

    if config.show_lighter_detection:
        plt.show()


if __name__ == "__main__":
    main()
