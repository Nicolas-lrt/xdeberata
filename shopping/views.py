from django.shortcuts import render, redirect

# Create your views here.
from account.decorators import admin_only
from account.models import Account, CartLine
from shopping.models import Product


def home_shop(request):
    produits = Product.objects.all()
    qtyTotal = 0
    client = Account.objects.filter(userId=request.user.id)
    if CartLine.objects.filter(client__in=client):
        cart = CartLine.objects.filter(client__in=client)
        for cart_line in cart:
            qtyTotal += cart_line.quantity
    admin = 0
    for group in request.user.groups.all():
        if group.name == 'admin':
            admin = 1
    context = {'products': produits, 'cartQty': qtyTotal, 'admin': admin}

    return render(request, 'shopping/home-shop.html', context)


@admin_only
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('home-shop')

