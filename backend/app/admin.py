from django.contrib import admin

from .models import Book, bookstore

admin.site.register(Book)

admin.site.register(bookstore)
