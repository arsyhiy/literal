from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q


import json

from .models import Book, BoardGame, Product, Author, Publisher, Order, OrderItem


def index(request):
    new_books = Book.objects.all().order_by("-created_at")[:8]

    popular_books = Book.objects.all().order_by("-sold_count")[:8]

    context = {
        "new_books": new_books,
        "popular_books": popular_books,
    }

    return render(request, "app/index.html", context)


# author
class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for a author."""

    model = Author


# publisher
class publisherDetailView(generic.DetailView):
    """Generic class-based detail view for a publisher."""

    model = Publisher


# product
class productsListView(generic.ListView):
    """Generic class-based view for a list of products."""

    model = Product
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    """Generic class-based detail view for a product."""

    model = Product


# board


class BoardGameListView(generic.ListView):
    """Generic class-based view for a list of board games."""

    model = BoardGame
    context_object_name = "boardgames"
    paginate_by = 10


class BoardGameDetailView(generic.DetailView):
    """Generic class-based detail view for a board game."""

    model = BoardGame


# book
class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""

    model = Book
    context_object_name = "books"
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""

    model = Book


def checkout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", {})

        order = Order.objects.create(total=0)

        total = 0

        for book_id, item in cart.items():
            # ✅ приведение типов
            quantity = int(item.get("quantity", 1))
            price = int(item.get("price", 0))

            total += price * quantity

            OrderItem.objects.create(
                order=order,
                product_name=item.get("title", ""),
                price=price,
                quantity=quantity,
            )

        order.total = total
        order.save()

        return JsonResponse({"status": "ok"})


def search(request):
    query = request.GET.get("q", "")

    results = (
        Book.objects.filter(Q(name__icontains=query) | Q(author__name__icontains=query))
        if query
        else []
    )

    return render(request, "app/search.html", {"query": query, "results": results})


def favorites(request):
    return render(request, "app/favorites.html")


def orders(request):
    return render(request, "app/orders.html")


def cart(request):
    return render(request, "app/cart.html")


@login_required
def profile(request):
    return render(request, "app/profile.html")
