import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1/')


# my tests
class TestAuthor(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.author1 = Author.objects.create(
                first_name='Kavian',
                last_name='AmirMozafari'
        )
        cls.author2 = Author.objects.create(
                first_name='Kavian',
                last_name='AmirMozafari',
                date_of_birth='1995-08-27'
        )

    # def setUp(self) -> None:
        # setUp: Run once for every test method to setup clean data.

    def test_none_birth_death(self):
        self.assertEqual(None, self.author1.date_of_birth)
        self.assertEqual(None, self.author1.date_of_death)

    def test_none_death(self):
        self.assertEqual(None, self.author1.date_of_death)

    def test_get_absolute_url(self):
        response = self.client.get(reverse('author-detail', args=[str(self.author1.id)]))
        response = response.content.decode('utf-8')
        self.assertIn(self.author1.first_name, response)
        self.assertIn(self.author1.last_name, response)

    def test_str(self):
        self.assertEqual(f'{self.author1.last_name}, {self.author1.first_name}', self.author1.__str__())

