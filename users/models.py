import uuid
from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    ABOUT_MAX_LENGTH,
    PHONE_MAX_LENGTH,
    USER_FIELD_MAX_LENGTH,
)

from .managers import UserManager


AVATAR_SIZE = 200
AVATAR_BACKGROUND = "#4A90E2"
AVATAR_TEXT_COLOR = "#FFFFFF"


class Skill(models.Model):
    name = models.CharField(
        "Название навыка",
        max_length=USER_FIELD_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None

    email = models.EmailField(
        "Адрес электронной почты",
        unique=True,
    )
    name = models.CharField(
        "Имя",
        max_length=USER_FIELD_MAX_LENGTH,
    )
    surname = models.CharField(
        "Фамилия",
        max_length=USER_FIELD_MAX_LENGTH,
    )
    avatar = models.ImageField(
        "Аватар",
        upload_to="avatars/",
        blank=True,
    )
    phone = models.CharField(
        "Телефон",
        max_length=PHONE_MAX_LENGTH,
        blank=True,
        null=True,
        unique=True,
    )
    github_url = models.URLField(
        "GitHub",
        blank=True,
    )
    about = models.TextField(
        "О себе",
        max_length=ABOUT_MAX_LENGTH,
        blank=True,
    )
    skills = models.ManyToManyField(
        Skill,
        verbose_name="Навыки",
        related_name="users",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        full_name = f"{self.name} {self.surname}".strip()
        return full_name or self.email

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar.save(
                self._get_avatar_filename(),
                self._generate_avatar(),
                save=False,
            )

        super().save(*args, **kwargs)

    def _get_avatar_filename(self):
        return f"avatar_{uuid.uuid4()}.png"

    def _generate_avatar(self):
        image = Image.new(
            "RGB",
            (AVATAR_SIZE, AVATAR_SIZE),
            color=AVATAR_BACKGROUND,
        )
        draw = ImageDraw.Draw(image)
        letter = self.name[0].upper()

        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except OSError:
            font = ImageFont.load_default()

        text_box = draw.textbbox((0, 0), letter, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        position = (
            (AVATAR_SIZE - text_width) / 2,
            (AVATAR_SIZE - text_height) / 2 - 10,
        )

        draw.text(
            position,
            letter,
            fill=AVATAR_TEXT_COLOR,
            font=font,
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        return ContentFile(buffer.getvalue())
