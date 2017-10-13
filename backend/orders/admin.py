from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model =         OrderItem
    raw_id_fields = ['book',]


class OrderAdmin(admin.ModelAdmin):
    # model = Order
    list_display = ['id', 
                    'first_name', 
                    'last_name', 
                    'email', 
                    'order_info',
                    'created']
    list_filter =  ['created', 
                    'updated']
    # allows you to click order and change it
    inlines =      [OrderItemInline]

    def order_info(self, obj):
        title =     [order.book.title for order in obj.items.all()]
        quantity =  [order.quantity for order in obj.items.all()]
        info =      list(zip(title, quantity))
        return info
        # return ", ".join(order.book.title for order in obj.items.all())
        # return title, quantity
        # return obj.item.book.title


admin.site.register(Order, OrderAdmin)
