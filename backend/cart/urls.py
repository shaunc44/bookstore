from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views



app_name = 'cart'
# print(dir(views.CartAdd))

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^$', views.BookList.as_view(), name='book_list'),
    url(r'^(?P<id>\d+)/$', views.BookDetail.as_view(), name='book_detail'),
    url(r'^cart/$', views.CartDetail.as_view(), name='cart_detail'),
    url(r'^add/(?P<book_id>\d+)/$', views.CartAdd.as_view(), name='cart_add'),
    url(r'^remove/(?P<book_id>\d+)/$', views.CartRemove.as_view(), name='cart_remove'),
    url(r'^order/$', views.OrderCreate.as_view(), name='order_create'),
    url(r'^order_created/$', views.OrderCreated.as_view(), name='order_created'),
    # url(r'^order/(?P<id>\d+)/$', views.OrderCreated.as_view(), name='order_created'),
    # url(r'^order/(?P<id>\d+)/$', views.OrderCreated.as_view(), name='order_created'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]




# admin.site.site_header = 'Dark Side of the Moon Books - Administration'


# USE ROUTER WITH VIEWSETS
# router = DefaultRouter()
# # router.register(r'books', views.BookList)
# router.register(r'books', views.BookViewSet)
# router.register(r'orders', views.OrderViewSet)
# router.register(r'orderitems', views.OrderItemViewSet)
# router.register(r'users', views.UserViewSet)