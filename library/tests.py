from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Author, Book
from datetime import date


class AuthorTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Иван',
            last_name='Иванов',
            country_of_birth='Россия',
            date_of_birth=date(1990, 1, 1),
        )

    def test_author_full_name(self):
        self.assertEqual(self.author.full_name(), 'Иван Иванов')

    def test_author_date_of_death_before_birth(self):
        with self.assertRaises(ValidationError) as context:
            self.author.date_of_death = date(1980, 12, 31)
            self.author.full_clean()
        self.assertTrue('Дата смерти не может быть раньше даты рождения.' in str(context.exception))

class BookTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Иван',
            last_name='Иванов',
            country_of_birth='Россия',
            date_of_birth=date(1990, 1, 1),
        )
        self.book = Book.objects.create(
            title='Пример книги',
            description='Описание книги',
        )
        self.book.authors.add(self.author)

    def test_book_title(self):
        self.assertEqual(self.book.title, 'Пример книги')

    def test_book_description(self):
        self.assertEqual(self.book.description, 'Описание книги')

    def test_book_has_author(self):
        self.assertEqual(self.book.authors.first().full_name(), 'Иван Иванов')
