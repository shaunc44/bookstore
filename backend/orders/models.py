from __future__ import unicode_literals

# from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from models import Book
from PIL import Image



class Book(models.Model):
    cover = models.ImageField(upload_to = 'static/images')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn_13 = models.CharField(max_length=13)
    author_first_name = models.CharField(max_length=20)
    author_last_name = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % (self.title,)

    def get_absolute_url(self):
        return reverse('cart:book_detail', args=[self.id])



class Order(models.Model):
    first_name =    models.CharField(max_length=50)
    last_name =     models.CharField(max_length=50)
    email =         models.EmailField()
    address =       models.CharField(max_length=100)
    postal_code =   models.CharField(max_length=20)
    city =          models.CharField(max_length=50)
    state =         models.CharField(max_length=50)
    # created_at =    models.DateTimeField(default=timezone.now)
    created =       models.DateTimeField(auto_now_add=True)
    updated =       models.DateTimeField(auto_now=True)
    paid =          models.BooleanField(default=False)
    customer =      models.ForeignKey(User)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order =     models.ForeignKey(Order, related_name='items')
    book =      models.ForeignKey(Book, related_name='order_items')
    price =     models.DecimalField(max_digits=10, decimal_places=2)
    quantity =  models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
