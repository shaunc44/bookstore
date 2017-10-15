from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from orders.models import Book, Order, OrderItem
from django.contrib.auth.models import User



class BookSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Book
        fields = ('url', 'id', 'cover', 'title', 'description', 
                  'price', 'isnb_13', 'language', 
                  'author_first_name', 'author_last_name')
        view_name = 'book-detail'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # how to link owner????
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Order
        fields = ('url', 'id', 'owner', 'first_name', 'last_name', 'email', 
                  'address', 'postal_code', 'city', 'state', 
                  'created', 'update', 'paid', 'customer')
        view_name = 'order-detail'


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    # these get passed into field

    class Meta:
        model = OrderItem
        fields = ('url', 'id', 'owner', 'order', 'book', 'price', 'quantity')
        view_name = 'orderitem-detail'
        # view_name = 'order-detail'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    # books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'orders') # 'books' ???





