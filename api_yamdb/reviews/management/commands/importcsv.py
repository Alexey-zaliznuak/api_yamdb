import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title


def read_csv(name):
    print(f'читаю файл {name}.csv')
    return pd.read_csv(f'static/data/{name}.csv')


def import_category():
    data = [
        Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        for i, row in read_csv("category").iterrows()
    ]
    Category.objects.bulk_create(data)


def import_genre():
    data = [
        Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        for i, row in read_csv("genre").iterrows()
    ]
    Genre.objects.bulk_create(data)

def import_titles():
    data = [
        Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(pk=row['category']),
        )
        for i, row in read_csv("titles").iterrows()
    ]
    Title.objects.bulk_create(data)

    for i, row in read_csv("genre_title").iterrows():
        title = Title.objects.get(pk=row['title_id'])
        genre = Genre.objects.get(pk=row['genre_id'])
        title.genre.add(genre)
class Command(BaseCommand):
    def handle(self, *args, **options):
        import_category()
        import_genre()
        import_titles()
        print('Импорт завершен!')
