import csv
import datetime
import os
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

PUB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class Command(BaseCommand):
    """Команда загружает тестовые данные в БД."""

    help = (
        'Загрузить данные из .csv файлов, расположенных в директории '
        'settings.CSV_FILES_DIR, в БД.'
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """
        Читает csv файлы, с помощью Django ORM создаёт объекты и сохраняет.
        """
        os.chdir(settings.CSV_FILES_DIR)
        reading_order = {
            'genre.csv': Genre,
            'category.csv': Category,
            'titles.csv': Title,
            'genre_title.csv': None,
            'users.csv': User,
            'review.csv': Review,
            'comments.csv': Comment,
        }
        integers = ('id', 'year', 'title_id', 'score', 'review_id')
        related_models = ('category', 'author')
        for file_name, klass in reading_order.items():
            with open(file_name, newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                if file_name == 'genre_title.csv':
                    for row in reader:
                        obj = Title.objects.get(id=int(row.get('title_id')))
                        obj.genre.add(
                            Genre.objects.get(id=int(row.get('genre_id')))
                        )
                        obj.save()
                else:
                    for row in reader:
                        for column in integers:
                            if column in row:
                                row[column] = int(row[column])
                        for column in related_models:
                            if column in row:
                                row[column + '_id'] = int(row.pop(column))
                        if 'pub_date' in row:
                            row['pub_date'] = datetime.datetime.strptime(
                                row['pub_date'], PUB_DATE_FORMAT
                            )
                        obj = klass(**row)
                        obj.save()
            print(f'{file_name} загружен.')
        print('Команда успешно закончила своё выполнение.')
