from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from PIL import Image



# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_initial = models.CharField(max_length=1)
    email = models.EmailField(max_length=75)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_initial)


class Book(models.Model):
    cover = models.ImageField(upload_to = 'static/images')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn_13 = models.CharField(max_length=13) 
    author_first_name = models.CharField(max_length=20)
    author_last_name = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return "%s - %s" % (self.title, self.price)

    def get_absolute_url(self):
        return reverse('api:book_detail', args=[self.id])



# class Cart(models.Model):
#     uid = models.ForeignKey(User)
#     pid = models.ForeignKey(Book)
#     no_item = models.IntegerField()

















