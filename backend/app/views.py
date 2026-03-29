from django.shortcuts import render
from django.views import generic
from .models import Book
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
    return render(request, "app/index.html")


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    context_object_name = "books"
    paginate_by = 10


@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', {})
        total = 0
        order_items = []

        for book_id, item in cart.items():
            try:
                book = Book.objects.get(pk=book_id)
                quantity = item.get('quantity', 1)
                total += book.price * quantity
                order_items.append({'title': book.title, 'quantity': quantity, 'price': book.price})
            except Book.DoesNotExist:
                continue

        # Здесь можно создать Order/OrderItem в базе, если нужно
        return JsonResponse({'status': 'ok', 'total': total, 'items': order_items})

    return JsonResponse({'status': 'error'}, status=400)
