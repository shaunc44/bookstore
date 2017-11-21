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
from django.http import HttpResponseRedirect



# ***************************************************************** #
#                            BOOK VIEWS                             #
# ***************************************************************** #

class BookList(APIView):
    # This viewset automatically provides `list` and `detail` actions.
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'book/list.html'

    def get(self, request):
        cart = Cart(request)
        queryset = Book.objects.all()

        return Response({
            'books': queryset, 
            'cart_len': cart.__len__(),
            'total_price': cart.get_total_price()
        })


class BookDetail(APIView):
    # This viewset automatically provides `list` and `detail` actions.
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'book/detail.html'

    def get(self, request, id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=id)
        cart_book_form = CartAddBookForm()

        return Response({ 
            'book': book,
            'cart_len': cart.__len__(),
            'cart_book_form': cart_book_form, 
            'total_price': cart.get_total_price()
        })


# ***************************************************************** #
#                            CART VIEWS                             #
# ***************************************************************** #

class CartDetail(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def get(self, request):
        cart = Cart(request)
        cart_list = list(cart)

        for item in cart_list:
            item['update_quantity_form'] = [field.as_widget() for field in CartAddBookForm(
                initial={
                    'quantity': item['quantity'],
                    'update':   True
                }
            )]

        return Response({
            'cart': cart_list,
            'cart_len': cart.__len__(),
            'total_price': cart.get_total_price()
        })


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
            item['update_quantity_form'] = [field.as_widget() for field in CartAddBookForm(
                initial={
                    'quantity': item['quantity'],
                    'update':   True
                }
            )]

        return Response({
            'book': book.data,
            'cart': cart_list,
            'cart_len': cart.__len__(),
            'total_price': cart.get_total_price(),
        })


class CartRemove(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'cart/detail.html'

    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.remove(book)

        book = BookSerializer(book, context=dict(request=request))
        cart_list = list(cart)

        for item in cart_list:
            item['update_quantity_form'] = [field.as_widget() for field in CartAddBookForm(
                initial={
                    'quantity': item['quantity'],
                    'update':   True
                }
            )]

        return Response({
            'book': book.data,
            'cart': cart_list,
            'cart_len': cart.__len__(),
            'total_price': cart.get_total_price()
        })


# ***************************************************************** #
#                            ORDER VIEW                             #
# ***************************************************************** #

class OrderCreate(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'orders/create.html'

    def get(self, request):
        # renderer_classes = (TemplateHTMLRenderer,)
        # template_name = 'orders/create.html'

        form = OrderCreateForm()
        cart = Cart(request)
        cart_list = list(cart)

        # for item in cart_list:
        return Response({
            'form': form,
            'cart': cart_list,
            'cart_len': cart.__len__(),
            'total_price': cart.get_total_price()
        })

# Try to make this a different view class, add url orderCreated ... *******
    def post(self, request):
        # renderer_classes = (TemplateHTMLRenderer,)
        # template_name = 'orders/created.html'

        cart = Cart(request)
        # print ("Cart:", cart)
        cart_list = list(cart)
        # print ("Cart List:", cart_list)

        # form = OrderCreateForm(request.POST, instance=profile)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in cart_list:
                print ("\nItem:", item, "\n")
                OrderItem.objects.bulk_create([
                    OrderItem(
                        order = order,
                        book = get_object_or_404(Book, id=item['book']['id']),
                        # book = item['book'],
                        price = item['total_price'],
                        quantity = item['quantity']
                    )
                    # for item in cart_list
                ])

            # clear the cart
            cart.clear()

        return Response({
            'order': order,
            # 'orders/created.html'
        })



# class OrderCreated(APIView):
#     # This viewset automatically provides `list` and `detail` actions.
#     renderer_classes = (TemplateHTMLRenderer,)
#     template_name = 'orders/created.html'

#     def get(self, request):
#         order = Order(request)
#         # cart = Cart(request)
#         # queryset = Book.objects.all()

#         return Response({
#             'order': order.id
#             # 'books': queryset, 
#             # 'cart_len': cart.__len__(),
#             # 'total_price': cart.get_total_price()
#         })







# class OrderCreated(APIView):
#     renderer_classes = (TemplateHTMLRenderer,)
#     template_name = 'orders/created.html'
#     # def order_create(self, request):
#     def post(self, request):
#         cart = Cart(request)
#         cart_list = list(cart)
#         # print ("Cart List:", cart_list)
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart_list:
#                 OrderItem.objects.create(
#                     order =    order,
#                     book =     item['book'],
#                     price =    item['price'],
#                     quantity = item['quantity']
#                 )
#             # clear the cart
#             cart.clear()
#             # return render(request,
#             #              'orders/created.html', 
#             #              {'order': order})
#         return Response({
#             #'cart': cart_list,
#             'order': order.id
#         })
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
