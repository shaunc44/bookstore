from __future__ import unicode_literals

from django.db import models
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


class Product(models.Model):
    cover = models.ImageField(upload_to = 'static/images')
    # cover = models.ImageField(upload_to = 'images', default='images/no_image.gif')
    # def image_tag(self):
    #     return mark_safe( '<img src="images/%s" width="132 height="200" />' % (self.cover) )
    # image_tag.short_description = "Image"
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn_13 = models.CharField(max_length=100) 
    author_first_name = models.CharField(max_length=30)
    author_last_name = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return "%s - %s" % (self.title, self.price)


class Cart(models.Model):
    uid = models.ForeignKey(User)
    pid = models.ForeignKey(Product)
    no_item = models.IntegerField()

















