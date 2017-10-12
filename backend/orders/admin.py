from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model =         OrderItem
    # list_display =  ['get_book_title']
    raw_id_fields = ['book',]


# class OrderItemAdmin(admin.ModelAdmin):
#     list_display =  ['get_book_title']
#     def get_book_title(self, obj):
#         return obj.book.title


class OrderAdmin(admin.ModelAdmin):
    # model = Order
    list_display = ['id', 
                    'first_name', 
                    'last_name', 
                    'email', 
                    'created']
    list_filter =  ['created', 
                    'updated']
    inlines =      [OrderItemInline]


admin.site.register(Order, OrderAdmin)
