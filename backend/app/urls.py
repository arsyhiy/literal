from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import BookDetailView, index, BookListView, checkout

urlpatterns = [
    # home
    path(
        "", RedirectView.as_view(url="/index/", permanent=False)
    ),  # если нет ничего кроме http://127.0.0.1:8000 редирект к index
    path("index/", index, name="index"),  # что бы можно отсылать по названию


    # book
    # keep in mind that url would look like:
    # http://127.0.0.1:8000/book/63070bff-3947-403c-b29b-adb68d624711/
    path("book/<uuid:pk>/", BookDetailView.as_view(), name="book-detail"),
    # catalog
    path("catalog/", BookListView.as_view(),
         name="catalog"),  # список всех книг


    # login/logout
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "accounts/logged_out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),
    # basket
    path("checkout/", checkout, name="checkout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
