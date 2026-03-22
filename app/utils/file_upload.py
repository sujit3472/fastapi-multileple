import os
import uuid
from fastapi import UploadFile

BASE_UPLOAD_DIR = "uploads"

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "image/gif",
]

ALLOWED_EXT = ["jpg", "jpeg", "png", "gif", "webp"]

MAX_SIZE = 2 * 1024 * 1024  # 2MB


def save_image(
    image: UploadFile | None,
    folder: str,
    old_filename: str | None = None,
):

    if not image:
        return old_filename

    # ✅ validate type
    if image.content_type not in ALLOWED_TYPES:
        raise ValueError("Only image files allowed")

    ext = image.filename.split(".")[-1].lower()

    # ✅ validate extension
    if ext not in ALLOWED_EXT:
        raise ValueError("Invalid file extension")

    contents = image.file.read()

    # ✅ size validation
    if len(contents) > MAX_SIZE:
        raise ValueError("Image must be less than 2MB")

    upload_dir = os.path.join(BASE_UPLOAD_DIR, folder)

    os.makedirs(upload_dir, exist_ok=True)

    # ✅ unique name
    filename = f"{uuid.uuid4()}.{ext}"

    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    # ✅ delete old file
    if old_filename:
        old_path = os.path.join(upload_dir, old_filename)

        if os.path.exists(old_path):
            os.remove(old_path)

    return filename