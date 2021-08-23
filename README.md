# django_library

"Library" website written in Django and deployed on Heroku.

Website: [hidden-tor-68514.herokuapp.com](https://hidden-tor-68514.herokuapp.com).

## Overview

This web application creates an online catalog for a small library, where users can browse available books and manage their accounts.

The main features that have currently been implemented are:

* There are models for books, book copies, genre, language and authors.
* Users can view list and detail information for books and authors.
* Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).
* Librarians can renew reserved books

![Local Library Model](https://raw.githubusercontent.com/mdn/django-locallibrary-tutorial/master/catalog/static/images/local_library_model_uml.png)

