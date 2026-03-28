from django.urls import path, include

from .views import BookDetailView, index, BookListView
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/index/', permanent=False)),
    path('index/', index, name='index'),
    # keep in mind that url would look like: http://127.0.0.1:8000/book/63070bff-3947-403c-b29b-adb68d624711/
    path('book/<uuid:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('catalog/', BookListView.as_view(), name='catalog'),  # список всех книг
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logged_out/', TemplateView.as_view(template_name='registration/logged_out.html'), name='logged_out'),

]
