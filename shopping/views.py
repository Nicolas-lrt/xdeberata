import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView
from slugify import slugify

from account.decorators import admin_only
from account.models import Account, CartLine
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
