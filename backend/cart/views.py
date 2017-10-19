from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddBookForm
from orders.models import Book, Order, OrderItem
from orders.forms import OrderCreateForm

from cart.serializers import BookSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
# from cart.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
# from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.views import APIView


# ***************************************************************** #
#                            BOOK VIEWS                             #
# ***************************************************************** #

class BookList(APIView):
    # This viewset automatically provides `list` and `detail` actions.
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'book/list.html'

    def get(self, request):
        queryset = Book.objects.all()
        return Response( {'books': queryset} )


class BookDetail(APIView):
    # This viewset automatically provides `list` and `detail` actions.
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'book/detail.html'

    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        cart_book_form = CartAddBookForm()
        return Response( {'book': book,
                          'cart_book_form': cart_book_form} )


# ***************************************************************** #
#                             CART VIEW                             #
# ***************************************************************** #

class CartAdd(APIView):

    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    # @require_POST
    def post(self, request, book_id):
        # def cart_add(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        # print ("Book=", book)
        form = CartAddBookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(book =             book,
                     quantity =         cd['quantity'],
                     update_quantity =  cd['update'])
        # return redirect('cart:cart_detail')
        return Response( {'book': book,
                          'cart': cart} )


# @require_POST
# def post(self, request, book_id):
# # def cart_add(self, request, book_id):
#     cart = Cart(request)
#     book = get_object_or_404(Book, id=book_id)
#     form = CartAddBookForm(request.POST)

#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(book =             book,
#                  quantity =         cd['quantity'],
#                  update_quantity =  cd['update'])
#     # return redirect('cart:CartDetail.cart_detail')
#     # return Response( 'cart:cart_detail')
#     return redirect('cart:CartDetail')


class CartRemove(APIView):

    def cart_remove(request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.remove(book)
        return redirect('cart:cart_detail')


class CartDetail(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def cart_detail(request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddBookForm(
                initial={
                    'quantity': item['quantity'],
                    'update':   True
                }
            )
        return Response({'cart': cart})


class OrderCreate(APIView):

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




# ***************************************************************** #
#                         OLD BOOK VIEWSET                          #
# ***************************************************************** #


# class BookViewSet(viewsets.ModelViewSet): # use ReadOnlyViewSet here??

#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)



    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # def book_list(request):
    #     books = Book.objects.filter()

    #     return render(request, 
    #                   'book/list.html', 
    #                  {'books': books})


    # @list_route()
    # def book_detail(request, id):
    #     book = get_object_or_404(Book, id=id)
    #     cart_book_form = CartAddBookForm()
    #     return render(request, 
    #                   'book/detail.html',
    #                  {'book': book,
    #                   'cart_book_form': cart_book_form})



# ***************************************************************** #
#                       VIEW USING VIEWSETS                         #
# ***************************************************************** #


# class BookViewSet(viewsets.ReadOnlyModelViewSet):
# #     """
# #     This viewset automatically provides `list` and `detail` actions.
# #     """
#         queryset = Book.objects.filter()
#         serializer = BookSerializer(queryset, many=True)


# class OrderViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


# class OrderItemViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """
#     queryset = User.objects.all()
    # serializer_class = UserSerializer
