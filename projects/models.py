from django.conf import settings
from django.db import models


class Project(models.Model):

    class Status(models.TextChoices):
        OPEN = "open", "Открытый"
        CLOSED = "closed", "Закрытый"

    name = models.CharField(
        "Название проекта",
        max_length=200,
    )
    description = models.TextField(
        "Описание проекта",
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        related_name="owned_projects",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    github_url = models.URLField(
        "Ссылка на GitHub",
        blank=True,
    )
    status = models.CharField(
        "Статус",
        max_length=6,
        choices=Status.choices,
        default=Status.OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Участники",
        related_name="participated_projects",
        blank=True,
    )

    # Избранное оставляем, потому что оно есть в основном задании.
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="В избранном у пользователей",
        related_name="favorite_projects",
        blank=True,
    )

    updated_at = models.DateTimeField(
        "Дата обновления",
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name