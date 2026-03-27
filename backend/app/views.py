from django.shortcuts import render
from django.views import generic
from .models import Book

# def index(request):


#     book = Book
#     return render(
#             request,
#             'app/index.html',
#             context={'books': book,},

#             )


def index(request):
    return render(request, "app/index.html")


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    context_object_name = "books"     # чтобы в шаблоне был "books", как в функции
    paginate_by = 10
