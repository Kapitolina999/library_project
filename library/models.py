from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy

from library.validators import validate_first_num_phone, LenPhoneValidator


class Author(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    photo = models.ImageField(upload_to='photo', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True)
    page = models.PositiveSmallIntegerField(verbose_name='Количество страниц')
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество экземпляров', default=1)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']

    def __str__(self):
        return self.title


class User(AbstractUser):
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    username = models.PositiveBigIntegerField(gettext_lazy('username'), unique=True,
                                              help_text='Введите номер в формате 79990000000',
                                              validators=[LenPhoneValidator(11), validate_first_num_phone],
                                              error_messages=
                                              {'unique': gettext_lazy('A user with that username already exists.')}
                                              )
    book = models.ManyToManyField(Book, verbose_name='Активные книги', blank=True, related_name='users')
    date_joined = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def display_book(self):
        return ', '.join([book.title for book in self.book.all()])

    display_book.short_description = 'Книги'

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
