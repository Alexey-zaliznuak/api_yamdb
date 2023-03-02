from datetime import datetime

from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                                   message='invalid slug.')]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                                   message='invalid slug.')]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=[MaxValueValidator(datetime.now().year),
                    MinValueValidator(0)]
    )
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True
    )
    # rating = models.IntegerField(
    #     verbose_name='Рейтинг',
    #     validators=[MaxValueValidator(10),
    #                 MinValueValidator(0)],
    #     default=0,)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
