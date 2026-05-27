import re
from urllib.parse import urlparse

from django import forms

from .constants import GITHUB_HOSTS


def normalize_phone(value):
    if not value:
        return None

    phone = re.sub(r"\D", "", value)

    if phone.startswith("7"):
        phone = f"8{phone[1:]}"

    if not re.fullmatch(r"8\d{10}", phone):
        raise forms.ValidationError(
            "Введите номер в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
        )

    return phone


def validate_github_url(value, message):
    if not value:
        return value

    host = urlparse(value).netloc.lower()

    if host not in GITHUB_HOSTS:
        raise forms.ValidationError(message)

    return value
