import os
from uuid import uuid4

from django.db import models
from django.urls import reverse


def image_rename(instance, filename):
    """Переименовывает загружаемые изображения"""
    _, ext = os.path.splitext(filename)
    name = uuid4().hex
    filename = "%s%s" % (name, ext)
    return os.path.join('images', filename)


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=30,
        help_text='Введите тег'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        """Строковое представление модели"""
        return self.name


class Language(models.Model):
    """Модель, представляющая язык книги"""
    name = models.CharField(
        max_length=200,
        help_text='Введите язык книги (русский, английский)'
    )

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        """Строковое представление модели"""
        return self.name


class Book(models.Model):
    """Модель, представляющая книгу"""
    title = models.CharField(
        max_length=200
    )
    author = models.ManyToManyField(
        'Author',
        related_name='book'
    )
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    summary = models.TextField(
        max_length=2000,
        help_text='Введите короткое описание содержимого книги'
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 символов '
        '<a href="https://www.isbn-international.org/content/what-isbn">'
        'ISBN</a>'
    )
    tag = models.ManyToManyField(
        Tag,
        blank=True,
        help_text='Выберите теги для этой книги'
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    year = models.SmallIntegerField(
        null=True,
        blank=True,
    )
    cover = models.ImageField(
        upload_to=image_rename,
        null=True,
        blank=True,
    )
    num_pages = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    def __str__(self):
        """Строковое представление модели"""
        return f'{self.title}'

    def get_absolute_url(self):
        """Возвращает url для доступа к детальной записи книги"""
        return reverse('book-detail', args=[str(self.id)])


class Author(models.Model):
    """Модель, представляющая автора"""
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    date_of_birht = models.DateField(
        null=True,
        blank=True
    )
    date_of_death = models.DateField(
        'Died',
        null=True,
        blank=True
    )
    picture = models.ImageField(
        upload_to=image_rename,
        null=True,
        blank=True,
    )
    about = models.TextField(
        max_length=2000,
        help_text='Об авторе',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self):
        """Строковое представление модели"""
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Возвращает url для доступа к детальной записи автора книги"""
        return reverse('author-detail', args=[str(self.id)])


class Publisher(models.Model):
    name = models.CharField(
        max_length=30
    )

    class Meta:
        verbose_name = 'издательство'
        verbose_name_plural = 'издательства'

    def __str__(self):
        """Строковое представление модели"""
        return self.name
