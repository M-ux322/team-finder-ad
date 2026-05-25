from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть адрес электронной почты.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Skill(models.Model):

    name = models.CharField(
        "Название навыка",
        max_length=100,
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
    avatar = models.ImageField(
        "Аватар",
        upload_to="avatars/",
        blank=True,
    )
    bio = models.TextField(
        "О себе",
        blank=True,
    )
    phone = models.CharField(
        "Телефон",
        max_length=30,
        blank=True,
    )
    github = models.URLField(
        "GitHub",
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
        return self.get_full_name() or self.email

    @property
    def name(self):
        return self.first_name

    @property
    def surname(self):
        return self.last_name

    @property
    def about(self):
        return self.bio

    @property
    def github_url(self):
        return self.github