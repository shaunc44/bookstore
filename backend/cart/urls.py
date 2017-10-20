from django.conf.urls import url, include
# from django.conf.urls import patterns
from . import views
from rest_framework.routers import DefaultRouter
# from rest_framework.schemas import get_schema_view


# USE ROUTER WITH VIEWSETS
# router = DefaultRouter()
# # router.register(r'books', views.BookList)
# router.register(r'books', views.BookViewSet)
# router.register(r'orders', views.OrderViewSet)
# router.register(r'orderitems', views.OrderItemViewSet)
# router.register(r'users', views.UserViewSet)

app_name = 'cart'
# print(dir(views.CartAdd))
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^$', views.BookList.as_view(), name='book_list'),
    url(r'^(?P<id>\d+)/$', views.BookDetail.as_view(), name='book_detail'),
    url(r'^cart/$', views.CartDetail.as_view(), name='cart_detail'), # this works
    url(r'^add/(?P<book_id>\d+)/$', views.CartAdd.as_view(), name='cart_add'), # does NOT work - API
    url(r'^remove/(?P<book_id>\d+)/$', views.CartRemove.as_view(), name='cart_remove'), # does NOT work - API
    url(r'^create/$', views.OrderCreate.as_view(), name='order_create'), # this works
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]




# urlpatterns = [
#     url(r'^$', views.book_list, name='book_list'),
#     # only works if i change namespace to API
#     url(r'(?P<id>\d+)/$', views.book_detail, name='book_detail'),
#     # only works if i change namespace to API
#     url(r'^cart/$', views.cart_detail, name='cart_detail'), # this works
#     url(r'^add/(?P<book_id>\d+)/$', views.cart_add, name='cart_add'), # does NOT work - API
#     url(r'^remove/(?P<book_id>\d+)/$', views.cart_remove, name='cart_remove'), # does NOT work - API
#     url(r'^create/$', views.order_create, name='order_create'), # this works
# ]