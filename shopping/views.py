import datetime

import stripe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView
from slugify import slugify

from account.decorators import admin_only
from account.models import Account, CartLine, Order, OrderDetail, Address
from account.views import isAdmin
from projet import settings
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
    context = {'products': produits, 'cartQty': getCartQty(request), 'admin': isAdmin(request)}

    return render(request, 'shopping/home-shop.html', context)


def shop_search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(mainDesc__icontains=search) |
                                          Q(shortDesc__icontains=search))
        context = {'products': products, 'search': search, 'cartQty': getCartQty(request)}
        return render(request, 'shopping/shop-search.html', context)


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


def taxes(request):
    client = Account.objects.filter(userId=request.user.id)
    for a in client:
        client = a
    if client.country == 'Canada':
        state = client.state
        if state == 'Alberta' or \
                state == 'Colombie-Britanique' or \
                state == 'Manitoba' or \
                state == 'Nanavut' or \
                state == 'Saskatchewan' or \
                state == 'Territoire-Nord-Ouest' or \
                state == 'Yukon':
            taxe = 5
        elif state == 'Ile-du-Prince-Edouard' or \
                state == 'Nouveau-Brunswick' or \
                state == 'Nouvelle-Ecosse' or \
                state == 'Terre-Neuve-et-Labrador':
            taxe = 15
        elif state == 'Ontario':
            taxe = 13
        elif state == 'Quebec':
            taxe = 14.975
        return taxe


@login_required(login_url='login')
def cartPage(request):
    total_ht = 0
    client = Account.objects.filter(userId=request.user.id)
    cart = CartLine.objects.filter(client__in=client)
    for a in client:
        client = a
    for cart_line in cart:
        total_ht += cart_line.total_ht()
    taxe = taxes(request)
    tot_taxe = total_ht * (taxe / 100)
    total = total_ht + tot_taxe

    context = {'cart': cart,
               'client': client,
               'total_ht': total_ht,
               'taxe': taxe,
               'tot_taxe': tot_taxe,
               'total': total,
               'qtyTotal': getCartQty(request)
               }
    return render(request, 'shopping/cart-page.html', context)


@login_required
def choose_address(request):
    client = Account.objects.get(userId=request.user.id)
    address = Address.objects.filter(client__id=request.user.id)
    adresse = 0
    gender = 0
    if address:
        adresse = address[0]
        gender = adresse.gender

    if request.method == 'POST':
        print(request.POST.get('same-adr'))
        if Address.objects.filter(client=client).exists():
            address = adresse
            address.gender = request.POST.get('gender')
            address.first_name = request.POST.get('first_name')
            address.last_name = request.POST.get('last_name')
            address.company = request.POST.get('company')
            address.address = request.POST.get('address')
            address.additional_address = request.POST.get('additional_address')
            address.postcode = request.POST.get('postcode')
            address.city = request.POST.get('city')
            address.phone = request.POST.get('phone')
            address.mobilephone = request.POST.get('mobilephone')
            address.workphone = request.POST.get('workphone')
            address.save()
            client.default_shipping_address = address

            if client.default_invoicing_address is None:
                client.default_invoicing_address = address
            if request.POST.get('same-adr'):
                client.default_invoicing_address = address

            client.save()
            return redirect('cart-recap')
        else:
            address = Address(client=client,
                              gender=request.POST.get('gender'),
                              first_name=request.POST.get('first_name'),
                              last_name=request.POST.get('last_name'),
                              company=request.POST.get('company'),
                              address=request.POST.get('address'),
                              additional_address=request.POST.get('additional_address'),
                              postcode=request.POST.get('postcode'),
                              city=request.POST.get('city'),
                              phone=request.POST.get('phone'),
                              mobilephone=request.POST.get('mobilephone'),
                              workphone=request.POST.get('workphone'))
            address.save()
            client.default_shipping_address = address
            if client.default_invoicing_address is None:
                client.default_invoicing_address = address
            client.save()
            return redirect('cart-recap')

    context = {'address': adresse, 'gender': gender, 'client': client}
    return render(request, 'shopping/choose-address.html', context)


@login_required
def choose_invoice(request):
    client = Account.objects.get(userId=request.user.id)
    address = Address.objects.filter(client__id=request.user.id)
    adresse = 0
    gender = 0
    if address:
        if address[1] is not None:
            adresse = address[1]
        else:
            adresse = address[0]
        gender = adresse.gender

    if request.method == 'POST':
        if address[1] is not None:
            address = adresse
            address.gender = request.POST.get('gender')
            address.first_name = request.POST.get('first_name')
            address.last_name = request.POST.get('last_name')
            address.company = request.POST.get('company')
            address.address = request.POST.get('address')
            address.additional_address = request.POST.get('additional_address')
            address.postcode = request.POST.get('postcode')
            address.city = request.POST.get('city')
            address.phone = request.POST.get('phone')
            address.mobilephone = request.POST.get('mobilephone')
            address.workphone = request.POST.get('workphone')
            address.save()
            client.default_invoicing_address = address
            client.save()
            return redirect('choose-address')
        else:
            address = Address(client=client,
                              gender=request.POST.get('gender'),
                              first_name=request.POST.get('first_name'),
                              last_name=request.POST.get('last_name'),
                              company=request.POST.get('company'),
                              address=request.POST.get('address'),
                              additional_address=request.POST.get('additional_address'),
                              postcode=request.POST.get('postcode'),
                              city=request.POST.get('city'),
                              phone=request.POST.get('phone'),
                              mobilephone=request.POST.get('mobilephone'),
                              workphone=request.POST.get('workphone'))
            address.save()
            client.default_invoicing_address = address
            client.save()
            return redirect('choose-address')

    context = {'address': adresse, 'gender': gender}
    return render(request, 'shopping/choose-invoice.html', context)


@login_required
def cart_recap(request):
    total_ht = 0
    client = Account.objects.filter(userId=request.user.id)
    cart = CartLine.objects.filter(client__in=client)
    for a in client:
        client = a
    for cart_line in cart:
        total_ht += cart_line.total_ht()
    taxe = taxes(request)
    tot_taxe = total_ht * (taxe / 100)
    total = total_ht + tot_taxe

    shipping = client.default_shipping_address
    invoice = client.default_invoicing_address

    context = {'cart': cart,
               'client': client,
               'total_ht': total_ht,
               'taxe': taxe,
               'tot_taxe': tot_taxe,
               'total': total,
               'qtyTotal': getCartQty(request),
               'shipping': shipping,
               'invoice': invoice,
               }
    return render(request, 'shopping/cart-recap.html', context)


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
    context = {'product': produit,
               'images': images,
               'cartQty': getCartQty(request),
               'admin': isAdmin(request)
               }
    return render(request, 'shopping/product-detail.html', context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        client = Account.objects.filter(userId=request.user.id)
        cart = CartLine.objects.filter(client__in=client)
        lineItems = []
        for cartLine in cart:
            i = 0
            lineItems += [
                {
                    'name': cartLine.product.name,
                    'quantity': cartLine.quantity,
                    'currency': 'eur',
                    'amount': str(int(cartLine.product.price * 100)),
                }
            ]
        total_ht = 0
        for a in client:
            client = a
        for cart_line in cart:
            total_ht += cart_line.total_ht()
        taxe = taxes(request)
        tot_taxe = total_ht * (taxe / 100)

        lineItems += [
            {
                'name': 'Taxes (' + str(client.state) + ') : ' + str(taxe) + '%',
                'quantity': 1,
                'currency': 'eur',
                'amount': str(int(tot_taxe * 100))
            }
        ]
        print(lineItems)
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'shop/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'shop/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=lineItems
                # line_items=[
                #     {
                #         'name': cartLine.product.nom,
                #         'quantity': cartLine.quantity,
                #         'currency': 'eur',
                #         'amount': str(int(cartLine.product.prixReel * 100)),
                #     }
                # ]
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'shopping/paySuccess.html'


class CancelledView(TemplateView):
    template_name = 'shopping/payCancelled.html'


@login_required
def createOrder(request):
    client = Account.objects.get(userId=request.user.id)
    cart = CartLine.objects.filter(client_id=client.id)
    if cart:
        order = Order(client_id=client.id,
                      order_date=datetime.datetime.now(),
                      shipping_address=client.default_shipping_address,
                      invoicing_address=client.default_invoicing_address,
                      status=Order.WAITING)
        order.save()

        for cartline in cart:
            order_detail = OrderDetail(order_id=order.id,
                                       product_id=cartline.product.id,
                                       qty=cartline.quantity,
                                       product_unit_price=cartline.product.price
                                       )
            order_detail.save()
        cart.delete()
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def orderPage(request):
    client = Account.objects.get(userId=request.user.id)
    orders = Order.objects.filter(client_id=client.id)

    return render(request, 'shopping/orders.html', {'orders': orders})


@login_required
def orderDetails(request, pk):
    order = Order.objects.get(id=pk)
    print(order.status)
    orderDetail = OrderDetail.objects.filter(order_id=order.id)
    return render(request, 'shopping/order-details.html', {'orderDetail': orderDetail,
                                                           'order': order,
                                                           'admin': isAdmin(request)})


@admin_only
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shopping/order-list-admin.html', {'orders': orders})


@admin_only
def order_list_search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        users = User.objects.filter(Q(username__icontains=search))
        accounts = Account.objects.filter(user__in=users)
        orders = Order.objects.filter(Q(client__in=accounts))
        context = {'search': search, 'orders': orders}
        return render(request, 'shopping/order-list-admin-search.html', context)
    else:
        return render(request, 'shopping/order-list-admin-search.html', {})


@admin_only
def order_list_search_id(request):
    if request.method == "POST":
        search = request.POST.get('search')
        orders = Order.objects.filter(Q(id=search))
        context = {'search': search, 'orders': orders}
        return render(request, 'shopping/order-list-admin-search-id.html', context)
    else:
        return render(request, 'shopping/order-list-admin-search-id.html', {})


@admin_only
def change_order_state(request, order_id, pk):
    order = Order.objects.get(id=order_id)
    if pk == 1:
        order.status = 'W'
    elif pk == 2:
        order.status = 'P'
    elif pk == 3:
        order.status = 'S'
    elif pk == 4:
        order.status = 'C'

    order.save()

    return redirect(request.META.get('HTTP_REFERER'))
