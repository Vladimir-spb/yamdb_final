from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import year_validator


class Category(models.Model):
    """Модель категории"""

    name = models.CharField(
        'Название категории', max_length=256, unique=True, db_index=True
    )
    slug = models.SlugField(
        'Слаг категории', max_length=50, unique=True, db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра"""

    name = models.CharField(
        'Название жанра', max_length=50, unique=True, db_index=True
    )
    slug = models.SlugField('Слаг жанра', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        'Название произведения', max_length=100, db_index=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания произведения',
        validators=[year_validator],
        db_index=True,
    )
    description = models.TextField(
        max_length=500, blank=True, verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='titles', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        'Содержание отзыва',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                limit_value=settings.MINVALUE,
                message='Оценка должна быть в пределах от 1 до 10',
            ),
            MaxValueValidator(
                limit_value=settings.MAXVALUE,
                message='Оценка должна быть в пределах от 1 до 10',
            ),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_author_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[: settings.RETURN_SYMBOL]


class Comment(models.Model):
    """Модель коментария к отзыву."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[: settings.RETURN_SYMBOL]
