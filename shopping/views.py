from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from slugify import slugify

from account.decorators import admin_only
from account.models import Account, CartLine
from shopping.forms import AddProductForm
from shopping.models import Product


def getCartQty(request):
    qtyTotal = 0
    client = Account.objects.filter(userId=request.user.id)
    if CartLine.objects.filter(client__in=client):
        cart = CartLine.objects.filter(client__in=client)
        for cart_line in cart:
            qtyTotal += cart_line.quantity

    return qtyTotal


def home_shop(request):
    produits = Product.objects.all()
    admin = 0
    for group in request.user.groups.all():
        if group.name == 'admin':
            admin = 1

    context = {'products': produits, 'cartQty': getCartQty(request), 'admin': admin}

    return render(request, 'shopping/home-shop.html', context)


@login_required(login_url='login')
def addToCart(request, pk, qty):
    client = Account.objects.get(user_id=request.user.id)
    if CartLine.objects.filter(product_id=pk, client_id=client.id).exists():
        cart_line = CartLine.objects.get(product_id=pk, client_id=client.id)
        cart_line.quantity += int(qty)
    else:
        cart_line = CartLine(product_id=pk, client_id=client.id, quantity=qty)
    cart_line.save()
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('home-shop'))


@login_required(login_url='login')
def removeFromCart(request, pk):
    client = Account.objects.get(user_id=request.user.id)
    cart_line = CartLine.objects.get(product_id=pk, client_id=client.id)
    cart_line.quantity -= 1
    if cart_line.quantity <= 0:
        cart_line.delete()
    else:
        cart_line.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def clearCartLine(request, pk):
    CartLine.objects.get(id=pk).delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def clearCart(request):
    client = Account.objects.get(userId=request.user.id)
    CartLine.objects.filter(client_id=client.id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def cartPage(request):
    total = 0
    client = Account.objects.filter(userId=request.user.id)
    cart = CartLine.objects.filter(client__in=client)
    for cart_line in cart:
        total += cart_line.total()
    print(request)

    return render(request, 'shopping/cart-page.html', {'cart': cart, 'total': total, 'qtyTotal': getCartQty(request)})


@admin_only
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('home-shop')


class AddProduct(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'shopping/add-product.html'
    success_url = reverse_lazy('home-shop')


def product_detail(request, pk):
    produit = Product.objects.get(id=pk)
    images = {
        produit.additionalImg1 or None,
        produit.additionalImg2 or None,
        produit.additionalImg3 or None,
        produit.additionalImg4 or None,
        produit.additionalImg5 or None,
        produit.additionalImg6 or None,
        produit.additionalImg7 or None,
        produit.additionalImg8 or None,
        produit.additionalImg9 or None,
    }
    context = {'product': produit, 'images': images, 'cartQty': getCartQty(request)}
    return render(request, 'shopping/product-detail.html', context)

# @admin_only
# def add_product(request):
#     form = AddProductForm()
#     if request.method == 'POST':
#         form = AddProductForm(request.POST)
#         if form.is_valid():
#             name = request.POST.get('name')
#             slug = slugify(name)
#             product = Product(name=name,
#                               slug_prod=slug,
#                               price=request.POST.get('price'),
#                               mainDesc=request.POST.get('mainDesc'),
#                               shortDesc=request.POST.get('shortDesc'),
#                               mainImg=request.FILES["mainImg"]
#                               )
#             product.tag.set(request.POST.get('tag'))
#             if request.FILES["additionalImg1"]:
#                 product.additionalImg1 = request.FILES["additionalImg1"]
#
#             if request.FILES["additionalImg2"]:
#                 product.additionalImg2 = request.FILES["additionalImg2"]
#
#             if request.FILES["additionalImg3"]:
#                 product.additionalImg3 = request.FILES["additionalImg3"]
#
#             if request.FILES["additionalImg4"]:
#                 product.additionalImg4 = request.FILES["additionalImg4"]
#
#             if request.FILES["additionalImg5"]:
#                 product.additionalImg5 = request.FILES["additionalImg5"]
#
#             if request.FILES["additionalImg6"]:
#                 product.additionalImg6 = request.FILES["additionalImg6"]
#
#             if request.FILES["additionalImg7"]:
#                 product.additionalImg7 = request.FILES["additionalImg7"]
#
#             if request.FILES["additionalImg8"]:
#                 product.additionalImg8 = request.FILES["additionalImg8"]
#
#             if request.FILES["additionalImg9"]:
#                 product.additionalImg9 = request.FILES["additionalImg9"]
#
#             product.save()
#
#             return redirect('home-shop')
#
#     return render(request, 'shopping/add-product.html', {'form': form})
