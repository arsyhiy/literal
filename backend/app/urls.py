from django.urls import path

from .views import BookDetailView, index, BookListView

urlpatterns = [
    path('', index, name='index'),
    path('book/<uuid:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('catalog', BookListView.as_view(), name='catalog'),  # список всех книг
]
