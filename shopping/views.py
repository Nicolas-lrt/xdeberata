from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from slugify import slugify

from account.decorators import admin_only
from account.models import Account, CartLine
from shopping.forms import AddProductForm
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


class AddProduct(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'shopping/add-product.html'
    success_url = reverse_lazy('home-shop')




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
