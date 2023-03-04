import pandas as pd
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, User, Review, Comment


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


def import_users():
    data = [
        User(
            id=row['id'],
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            bio=row['bio'],
            role=row['role'],
        )
        for i, row in read_csv("users").iterrows()
    ]
    User.objects.bulk_create(data)


def import_review():
    data = [
        Review(
            id=row['id'],
            text=row['text'],
            score=row['score'],
            pub_date=row['pub_date'],
            author=User.objects.get(pk=row['author']),
            title=Title.objects.get(pk=row['title_id']),
        )
        for i, row in read_csv("review").iterrows()
    ]
    Review.objects.bulk_create(data)


def import_comments():
    data = [
        Comment(
            review_id=row['review_id'],
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            pub_date=row['pub_date'],
        )
        for i, row in read_csv("comments").iterrows()
    ]
    Comment.objects.bulk_create(data)


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_users()
        import_category()
        import_genre()
        import_titles()
        import_review()
        import_comments()
        print('Импорт завершен!')
