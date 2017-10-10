from django.contrib import admin
from django.utils.html import format_html

from .models import Customer, Product


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_initial', 'email']
    list_editable = ['email']

    class Meta:
        model = Customer

admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        print(dir(obj.cover))
        return format_html( '<img src="{}" />'.format(obj.cover.url) )
    image_tag.short_description = "Image"

    list_display = ['image_tag', 'title', 'description', 'price', 
                    'isbn_13', 'author_last_name', 'author_first_name']
    list_editable = ['title', 'price', 'isbn_13', 'author_last_name']

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


# admin.site.register(Customer)