from django.urls import path

from .views import *

urlpatterns = [
    # Home Page
    path('', index, name='index'),

    # Book urls
    path('book/', BookList.as_view(), name='book-list'),
    path('book/add/', BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('book/<int:pk>/edit/', BookEdit.as_view(), name='book-edit'),
    path('book/<int:pk>/delete/', BookDelete.as_view(), name='book-delete'),
    path('book/<uuid:pk>/renew/', RenewBookLibrarian.as_view(), name='renew-book-librarian'),

    # Author urls
    path('author/', AuthorList.as_view(), name='author-list'),
    path('author/add/', AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('author/<int:pk>/edit/', AuthorEdit.as_view(), name='author-edit'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),


    path('my-books/', MyBooks.as_view(), name='my_books'),
    path('my-borrowed-books/', UserBorrowedBooks.as_view(), name='user_borrowed_books'),
    path('borrowed/', Borrowed.as_view(), name='all-borrowed'),

    path('test/', test),
]
