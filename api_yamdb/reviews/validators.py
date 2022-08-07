from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validator(value):
    """Проверяет, чтобы год произведения не был из будущего."""
    if value > timezone.now().year:
        raise ValidationError(
            ('%(value)s год больше текущего.'),
            params={'value': value},
        )
