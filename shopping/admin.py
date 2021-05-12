from django.contrib import admin

# Register your models here.
from shopping.models import Product, Tag

admin.site.register(Product)
admin.site.register(Tag)