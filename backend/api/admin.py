from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from orders.models import Book


admin.site.site_header = settings.ADMIN_SITE_HEADER


class BookAdmin(admin.ModelAdmin):
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        # print(dir(obj.cover))
        return format_html( '<img src="{}" />'.format(obj.cover.url) )
    image_tag.short_description = "Image"

    list_display =  ['image_tag', 'title', 'description', 'price', 
                     'isbn_13', 'author_last_name', 'author_first_name']
    list_editable = ['title', 'description', 'price', 'isbn_13', 
                     'author_last_name', 'author_first_name']

    class Meta:
        model = Book

admin.site.register(Book, BookAdmin)


# admin.site.register(Customer)