import logging
from pathlib import Path
import uuid
from step_3.video import detect_faces, get_image_thumbnails, save_images
from utils import config
from video_indexer import VideoIndexer
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

FORMAT = "%(asctime)s %(module)s  %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


ID_PATH = Path("/mnt/c/Users/dpalma/Desktop/ids")

if __name__ == "__main__":
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
    # build_person_group(face_client, PERSON_GROUP_ID, person_group_name, ID_PATH)
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
