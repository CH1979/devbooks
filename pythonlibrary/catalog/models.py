from django.db import models
from django.urls import reverse


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=30,
        help_text='Введите тег'
    )

    def __str__(self):
        """Строковое представление модели"""
        return self.name


class Language(models.Model):
    """Модель, представляющая язык книги"""
    name = models.CharField(
        max_length=200,
        help_text='Введите язык книги (русский, английский)'
    )

    def __str__(self):
        """Строковое представление модели"""
        return self.name


class Book(models.Model):
    """Модель, представляющая книгу"""
    title = models.CharField(
        max_length=200
    )
    author = models.ManyToManyField(
        'Author'
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
        'ISBN number</a>'
    )
    tag = models.ManyToManyField(
        Tag,
        help_text='Выберите теги для этой книги'
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True
    )
    cover = models.ImageField(
        null=True
    )
    num_pages = models.IntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        """Строковое представление модели"""
        return self.title

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
        null=True
    )
    about = models.TextField(
        max_length=2000,
        help_text='Об авторе'
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """Строковое представление модели"""
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Возвращает url для доступа к детальной записи автора книги"""
        return reverse('author-detail', args=[str(self.id)])
