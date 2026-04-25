from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    BookDetailView,
    index,
    BookListView,
    checkout,
    search,
    favorites,
    orders,
    cart,
    profile,
)

urlpatterns = [
    path("", RedirectView.as_view(url="/index/", permanent=False)),
    path("index/", index, name="index"),
    path("book/<uuid:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("catalog/", BookListView.as_view(), name="catalog"),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "accounts/logged_out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),
    path("checkout/", checkout, name="checkout"),
    path("search/", search, name="search"),
    path("favorites/", favorites, name="favorites"),
    path("orders/", orders, name="orders"),
    path("cart/", cart, name="cart"),
    path("profile/", profile, name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
