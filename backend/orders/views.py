# from django.shortcuts import render
# from .models import OrderItem
# from .forms import OrderCreateForm
# from .tasks import order_created
# from cart.cart import Cart


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST': # first request is GET ?????
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order      = order,
#                                          book       = item['book'],
#                                          price      = item['price'],
#                                          quantity   = item['quantity'])
#             # clear the cart
#             cart.clear()
#             # launch asynchronous task
#             # order_created.delay(order.id)
#             return render(request, 
#                          'orders/created.html', 
#                          {'order': order})
#     else:
#         form = OrderCreateForm()

#     return render(request, 
#                   'orders/create.html', 
#                   {'cart': cart, 'form': form})
