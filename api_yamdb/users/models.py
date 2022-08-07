from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширение модели User. Добавление полей role и bio."""

    role = models.CharField(
        choices=settings.USER_ROLE_CHOICES,
        max_length=32,
        default=settings.USER_ROLE,
        verbose_name='Роль',
    )
    bio = models.TextField(
        max_length=256, blank=True, null=True, verbose_name='Биография'
    )


class ConfirmationCode(models.Model):
    """Модель confirmation_code связанная с пользователем."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения",
        max_length=settings.CONFIRMATION_CODE_LENGTH,
    )
