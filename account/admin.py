from django.contrib import admin

# Register your models here.
from account.models import Account, CartLine, Order, OrderDetail

admin.site.register(Account)
admin.site.register(CartLine)
admin.site.register(Order)
admin.site.register(OrderDetail)