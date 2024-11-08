import fnmatch
import logging
import os
import subprocess

import settings
from PIL import Image

logger = logging.getLogger(__name__)


class Attachment:
    def __init__(self, file_path: str, thumbnails: list = None, description: str = ""):
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise ValueError(
                "file_path must be a string and point to an existing file."
            )
        self.file_path = file_path
        self.description = description
        self.thumbnails = []

        if thumbnails:
            if not isinstance(thumbnails, list):
                raise ValueError("thumbnails must be a list of paths.")

            valid_thumbnails = []

            for thumbnail_path in thumbnails:
                if len(valid_thumbnails) >= 3:
                    break

                if not os.path.isfile(thumbnail_path):
                    logger.warning(f"File {thumbnail_path} does not exist.")
                    break
                if not thumbnail_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    logger.warning(
                        f"File {thumbnail_path} must be in JPG or PNG format."
                    )
                    break

                try:
                    with Image.open(thumbnail_path) as img:
                        if img.size[0] > 512 or img.size[1] > 512:
                            logger.warning(
                                f"Image {thumbnail_path} exceeds the maximum size of 512x512 pixels."
                            )
                            break
                except Exception as e:
                    logger.warning(f"Could not open image {thumbnail_path}. Error: {e}")
                    break
                valid_thumbnails.append(thumbnail_path)

            self.thumbnails = valid_thumbnails[:3]


def generate_thumbnails(thumbnail_dir, file_path):
    res_code = subprocess.call(
        [settings.MIRADA_PATH, "--mode", "thumb", file_path, "--temp", thumbnail_dir]
    )
    if res_code != 0:
        raise Exception(
            "Mirada returned a non-zero exit status.\n" + settings.MIRADA_PATH
        )

    thumbnails = []
    for f in os.listdir(thumbnail_dir):
        if fnmatch.fnmatch(f, os.path.basename(file_path) + ".thumb--3-*.jpg"):
            thumbnails.append(os.path.join(thumbnail_dir, f))

    thumbnails.sort()
    return thumbnails
    return thumbnails
