from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

from .models import Book, BoardGame, Product, Author, Publisher

# index
def index(request):  # пока такой пустой не знаю что даже делать.
    return render(request, "app/index.html")


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


@csrf_exempt
def checkout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", {})
        payment_method = data.get("payment_method", "unknown")
        total = 0
        order_items = []

        for book_id, item in cart.items():
            try:
                book = Book.objects.get(pk=book_id)
                quantity = item.get("quantity", 1)
                total += book.price * quantity
                order_items.append(
                    {"title": book.title, "quantity": quantity, "price": book.price}
                )
            except Book.DoesNotExist:
                print(f"Book {book_id} not found")
                continue

        # --- STUB: печатаем заказ и метод оплаты ---
        print("=== New Order ===")
        print(f"Payment method: {payment_method}")
        print("Items:")
        for it in order_items:
            print(f"- {it['title']} x {it['quantity']} = ${it['price']*it['quantity']}")
        print(f"Total: ${total:.2f}")
        print("================")

        # Возвращаем подтверждение клиенту
        return JsonResponse({"status": "ok", "total": total, "items": order_items})

    return JsonResponse({"status": "error"}, status=400)
