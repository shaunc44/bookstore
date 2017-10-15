# from django.conf.urls import url, include
# # from django.conf.urls import patterns
# from . import views
# from rest_framework.routers import DefaultRouter
# # from rest_framework.schemas import get_schema_view


# # router = DefaultRouter()
# # router.register(r'snippets', views.BookViewSet)
# # router.register(r'users', views.UserViewSet)



# app_name = 'api'

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








#-------------------------------------------------------------------#
#                       URLS (ORIGINAL SETUP)                       #
#-------------------------------------------------------------------#

# from django.conf.urls import url
# from . import views

# app_name = 'api'

# urlpatterns = [
#     url(r'^$', views.book_list, name='book_list'),
#     # url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
#     url(r'(?P<id>\d+)/$', views.book_detail, name='book_detail'),
# ]