from urllib.parse import urlparse

from django import forms

from .constants import GITHUB_HOSTS


def validate_github_url(value, message):
    if not value:
        return value

    host = urlparse(value).netloc.lower()

    if host not in GITHUB_HOSTS:
        raise forms.ValidationError(message)

    return value
