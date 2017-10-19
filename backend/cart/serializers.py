from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from orders.models import Book, Order, OrderItem
from django.contrib.auth.models import User



class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = ('url', 'id', 'cover', 'title', 
                  'description', 'price', 'isbn_13', 
                  'author_first_name', 'author_last_name')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # how to link owner????
    # books = serializers.HyperlinkedIdentityField(view_name='book-detail', format='html')
    items = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True) 

    class Meta:
        model = Order
        # add owner to fields, uncomment owner variable above
        fields = ('url', 'id', 'owner', 'first_name', 'last_name', 'email', 
                  'address', 'postal_code', 'city', 'state', 
                  'created', 'updated', 'paid', 'customer', 'items')


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # books = serializers.HyperlinkedIdentityField(view_name='book-detail', format='html')
    # these get passed into field

    class Meta:
        model = OrderItem
        # add owner to fields, uncomment owner variable above
        fields = ('url', 'id', 'owner', 'order', 'book', 'price', 'quantity')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # order_set = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    # orderitem_set = orderitem_set.order

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'order_set') # 'books' ???





