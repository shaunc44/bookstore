from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core import serializers
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
import json


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
#                            CART VIEWS                             #
# ***************************************************************** #

class CartDetail(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddBookForm(
                initial={
                    'quantity': item['quantity'],
                    'update':   True
                }
            )
        cart_list = list(cart)

        for item in cart_list:
            item["book"] = item["book"](request)

        return Response({'cart': cart_list, 
                         'total_price': cart.get_total_price()} )


class CartAdd(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        form = CartAddBookForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(book =             book,
                     quantity =         cd['quantity'],
                     update_quantity =  cd['update'])

        book = BookSerializer(book, context=dict(request=request))
        cart_list = list(cart)

        for item in cart_list:
            item["book"] = item["book"](request)

        return Response( {'book': book.data,
                          'cart': cart_list,
                          'total_price': cart.get_total_price()} )


class CartRemove(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def post(self, request, book_id):
        # print ("You are here")
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.remove(book)

        book = BookSerializer(book, context=dict(request=request))
        cart_list = list(cart)

        for item in cart_list:
            item["book"] = item["book"](request)

        return Response( {'book': book.data,
                          'cart': cart_list } )


# ***************************************************************** #
#                            ORDER VIEW                             #
# ***************************************************************** #

class OrderCreate(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'orders/create.html'

    # def order_create(self, request):
    def post(self, request):
        cart = Cart(request)
        cart_list = list(cart)
        print ("Cart List:", cart_list)
        # if request.method == 'POST':
        # form = OrderCreateForm(request.POST)
        form = OrderCreateForm()
        if form.is_valid():
            order = form.save()
            # for item in cart:
            for item in cart_list:
                OrderItem.objects.create(
                    order =    order,
                    book =     item['book'],
                    price =    item['price'],
                    quantity = item['quantity']
                )
            # clear the cart
            cart.clear()
            # return render(request,
            #              'orders/created.html', 
            #              {'order': order})
        return Response({'cart': cart_list,
                         'order': order})
        # else:
        #     form = OrderCreateForm()

        # # return render(request, 
        # #               'orders/create.html', 
        # #               {'cart': cart, 'form': form})
        # return Response('orders/create.html', 
        #                {'cart': cart, 
        #                 'form': form})


# class OrderCreated(APIView):
#     renderer_classes = (TemplateHTMLRenderer,)
#     # template_name = 'orders/create.html'

#     # def order_create(self, request):
#     def post(self, request):
#         cart = Cart(request)
#         if request.method == 'POST':
#             form = OrderCreateForm(request.POST)
#             if form.is_valid():
#                 order = form.save()
#                 for item in cart:
#                     OrderItem.objects.create(
#                         order =    order,
#                         book =     item['book'],
#                         price =    item['price'],
#                         quantity = item['quantity']
#                     )
#                 # clear the cart
#                 cart.clear()
#                 # return render(request, 
#                 #              'orders/created.html', 
#                 #              {'order': order})
#                 return Response('orders/created.html',
#                                {'order': order})
#         else:
#             form = OrderCreateForm()

#         # return render(request, 
#         #               'orders/create.html', 
#         #               {'cart': cart, 'form': form})
#         return Response('orders/create.html', 
#                        {'cart': cart, 
#                         'form': form})












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
