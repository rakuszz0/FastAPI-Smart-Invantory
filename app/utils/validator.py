import re


def validate_email(email: str):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email) is not None


def validate_phone(phone: str):

    pattern = r'^\+?\d{10,15}$'

    return re.match(pattern, phone) is not None


def validate_password(password: str):

    """
    Minimum:
    - 8 karakter
    - huruf besar
    - huruf kecil
    - angka
    """

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True