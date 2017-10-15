# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddBookForm
from orders.models import Book, Order, OrderItem
from orders.forms import OrderCreateForm

from cart.serializers import BookSerializer, UserSerializer, OrderSerializer, OrderItemSerializer
from cart.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
# from rest_framework.reverse import reverse
from django.contrib.auth.models import User





class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def book_list(request):
        books = Book.objects.filter()

        return render(request, 
                      'book/list.html', 
                     {'books': books})


    def book_detail(request, id):
        book = get_object_or_404(Book, id=id)
        cart_book_form = CartAddBookForm()
        return render(request, 
                      'book/detail.html',
                     {'book': book,
                      'cart_book_form': cart_book_form})


# Cart Views
@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    print ("Book=", book)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book =             book,
                 quantity =         cd['quantity'],
                 update_quantity =  cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(
            initial={
                'quantity': item['quantity'],
                'update':   True
            }
        )
    return render(request, 
                  'cart/detail.html', 
                  {'cart': cart})


# Old Orders views
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST': # should first request be GET ?????
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order =    order,
                                         book =     item['book1'],
                                         price =    item['price'],
                                         quantity = item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request, 
                         'orders/created.html', 
                         {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 
                  'orders/create.html', 
                  {'cart': cart, 'form': form})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

