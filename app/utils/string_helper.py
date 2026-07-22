import re
import uuid
import secrets


def slugify(
    text: str
):

    text = text.lower()

    text = re.sub(
        r'[^a-z0-9]+',
        '-',
        text
    )

    return text.strip('-')


def generate_uuid():

    return str(
        uuid.uuid4()
    )


def random_token(
    length: int = 32
):

    return secrets.token_hex(
        length
    )


def capitalize_words(
    text: str
):

    return text.title()