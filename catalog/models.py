from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
import uuid


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Genre(models.Model):
    name = models.CharField(max_length=20, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50, help_text='Book Title')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, related_name='books', help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    class LoanStatus(models.TextChoices):
        MAINTENANCE = 'm', 'Maintenance'
        ON_LOAN = 'o', 'On loan'
        AVAILABLE = 'a', 'Available'
        RESERVED = 'r', 'Reserved'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LoanStatus.choices, default=LoanStatus.AVAILABLE,
                              blank=True, help_text='Book availability')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=20)
    borrower = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def days_left(self):
        if self.due_back:
            return abs((self.due_back - date.today()).days)
        return None

    def __str__(self):
        return f'{self.id} ({self.book.title})'
