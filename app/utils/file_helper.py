import os
import uuid

from fastapi import UploadFile


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
}

MAX_FILE_SIZE = 5 * 1024 * 1024


def get_extension(
    filename: str
):

    return os.path.splitext(
        filename
    )[1].lower()


def is_allowed_file(
    filename: str
):

    return (
        get_extension(filename)
        in ALLOWED_EXTENSIONS
    )


def generate_filename(
    filename: str
):

    ext = get_extension(filename)

    return f"{uuid.uuid4()}{ext}"


async def validate_upload(
    file: UploadFile
):

    if not is_allowed_file(file.filename):

        raise ValueError(
            "File type not allowed"
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise ValueError(
            "File exceeds maximum size"
        )

    await file.seek(0)

    return True