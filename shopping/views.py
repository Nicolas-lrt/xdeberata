from django.shortcuts import render

# Create your views here.
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

    context = {'products': produits, 'cartQty': qtyTotal}

    return render(request, 'shopping/home-shop.html', context)
