from django.shortcuts import render, get_object_or_404
from .models import Book
from cart.forms import CartAddBookForm



# Create your views here.
def book_list(request):
    books = Book.objects.filter()
    return render(request, 
                  'api/book/list.html', 
                 {'books': books})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    cart_book_form = CartAddBookForm()
    return render(request, 
                  'api/book/detail.html',
                 {'book': book,
                  'cart_book_form': cart_book_form})