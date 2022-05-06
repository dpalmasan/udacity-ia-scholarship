import glob
import io
import logging
import sys
import time
import os
from video_indexer import VideoIndexer
from PIL import Image
from pathlib import Path
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType

from utils import config, get_log_level


FORMAT = "%(asctime)s %(module)s  %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(get_log_level(config.log_level))


def upload_video(indexer: VideoIndexer) -> str:
    uploaded_video_id = indexer.upload_to_video_indexer(
        input_filename="/mnt/c/Users/dpalma/Desktop/ids/udacity-video.mp4",
        video_name="dpalma-30-second",
        video_language="English",
    )
    return uploaded_video_id


def get_image_thumbnails(indexer: VideoIndexer, video_id: str):
    info = indexer.get_video_info(video_id, video_language="English")
    images = []
    img_raw = []
    img_strs = []
    for each_thumb in info["videos"][0]["insights"]["faces"][0]["thumbnails"]:
        if "fileName" in each_thumb and "id" in each_thumb:
            thumb_id = each_thumb["id"]
            img_code = indexer.get_thumbnail_from_video_indexer(
                video_id, thumb_id
            )
            img_strs.append(img_code)
            img_stream = io.BytesIO(img_code)
            img_raw.append(img_stream)
            img = Image.open(img_stream)
            images.append(img)

    return images, info


def save_images(path: Path, images, prefix="human-face"):
    for i, img in enumerate(images, start=1):
        img.save(path / f"{prefix}{i}.jpg")


def build_person_group(
    client: FaceClient,
    person_group_id,
    pgp_name,
    path: Path,
    prefix="human-face",
):
    logger.debug("Create and build a person group...")
    # Create empty Person Group. Person Group ID must be lower case,
    # alphanumeric, and/or with '-', '_'.
    logger.debug(f"Person group ID: {person_group_id}")
    client.person_group.create(
        person_group_id=person_group_id, name=person_group_id
    )

    # Create a person group person.
    human_person = client.person_group_person.create(person_group_id, pgp_name)
    # Find all jpeg human images in working directory.
    human_face_images = [
        file
        for file in glob.glob(str(path / "*.jpg"))
        if os.path.basename(file).startswith(prefix)
    ]
    # Add images to a Person object
    for image_p in human_face_images:
        with open(image_p, "rb") as w:
            client.person_group_person.add_face_from_stream(
                person_group_id, human_person.person_id, w
            )

    # Train the person group, after a Person object with many images
    # were added to it.
    client.person_group.train(person_group_id)

    # Wait for training to finish.
    while True:
        training_status = client.person_group.get_training_status(
            person_group_id
        )
        logger.debug("Training status: {}.".format(training_status.status))
        if training_status.status is TrainingStatusType.succeeded:
            break
        elif training_status.status is TrainingStatusType.failed:
            client.person_group.delete(person_group_id=person_group_id)
            sys.exit("Training the person group has failed.")
        time.sleep(5)


def detect_faces(client: FaceClient, query_images_list):
    logger.debug("Detecting faces in query images list...")

    face_ids = {}
    for image_path in query_images_list:
        image = open(image_path, "rb")
        logger.debug("Opening image: %s", image_path.stem)

        # Detect the faces in the query images list one at a time,
        # returns list[DetectedFace]
        try:
            faces = client.face.detect_with_stream(image)
        except Exception as e:
            if config.is_free_tier:
                logger.debug(f"{e}, will try to wait a minute")
                time.sleep(60)
                faces = client.face.detect_with_stream(image)
            else:
                raise

        # Add all detected face IDs to a list
        for face in faces:
            # Add the ID to a dictionary with image name as a key.
            # This assumes there is only one face per image (since you can't
            # have duplicate keys)
            face_ids[image_path.stem] = face.face_id

    return face_ids
