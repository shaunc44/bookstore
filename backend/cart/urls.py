from django.conf.urls import url
from . import views


app_name = 'cart'

urlpatterns = [
    url(r'^$', views.book_list, name='book_list'), # does NOT work
    url(r'(?P<id>\d+)/$', views.book_detail, name='book_detail'),
    url(r'^cart/$', views.cart_detail, name='cart_detail'), # this works
    url(r'^add/(?P<book_id>\d+)/$', views.cart_add, name='cart_add'), # does NOT work
    url(r'^remove/(?P<book_id>\d+)/$', views.cart_remove, name='cart_remove'), # does NOT work
    url(r'^create/$', views.order_create, name='order_create'), # this works
]