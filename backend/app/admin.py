from django.contrib import admin

from .models import Book, author

admin.site.register(Book)

admin.site.register(author)
