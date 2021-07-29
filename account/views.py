from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from account.decorators import unauthenticated_user, admin_only
from account.forms import CreateAccount
from account.models import Account, Address


def isAdmin(request):
    admin = 0
    for group in request.user.groups.all():
        if group.name == 'admin':
            admin = 1
    return admin


def logoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def sign_in(request):
    form = CreateAccount()
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get('username')).exists:
            messages.info(request, 'Nom d\'utilisateur déjà existant')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            # elif User.objects.filter(email=request.POST.get('email')).exists:
            #     messages.info(request, 'Email déjà associée à un autre compte')
            #     return redirect(request.META.get('HTTP_REFERER'))
            # form = CreateAccount(request.POST)
            # if form.is_valid():
            user = User(username=request.POST.get('username'),
                        password=request.POST.get('password'),
                        email=request.POST.get('email'),
                        first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name')
                        )
            user.save()
            account = Account(user_id=user.id,
                              country=request.POST.get('country'),
                              state=request.POST.get('state'))
            account.userId = user.id
            account.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'account/inscription.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # username = User.objects.get(email=email.lower()).username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Utilisateur et/ou Mot de passe incorrect(s)")
    return render(request, 'account/connexion.html')


@login_required
def my_account(request):
    client = Account.objects.get(userId=request.user.id)
    adresse = 0
    address = Address.objects.filter(client__id=request.user.id)
    for a in address:
        adresse = a

    context = {'address': adresse, 'account': client}
    return render(request, 'account/my-account.html', context)


@login_required
def change_last_name(request):
    if request.method == 'POST':
        last_name = request.POST.get('nom')
        request.user.last_name = last_name
        request.user.save()
        return redirect('my-account')
    return render(request, 'account/change-last_name.html')


@login_required
def change_first_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('prenom')
        request.user.first_name = first_name
        request.user.save()
        return redirect('my-account')
    return render(request, 'account/change-first_name.html')


@login_required
def change_email(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        request.user.email = mail
        request.user.save()
        return redirect('my-account')
    return render(request, 'account/change-email.html')


@login_required
def change_password(request):
    username = request.user.username
    if request.method == 'POST':
        pswd = request.POST.get('pswd')
        request.user.set_password(pswd)
        request.user.save()
        user = authenticate(request, username=username, password=pswd)
        login(request, user)
        return redirect('my-account')
    return render(request, 'account/change-password.html')


@login_required
def change_residence(request):
    client = Account.objects.get(userId=request.user.id)
    context = {'account': client}
    if request.method == 'POST':
        client.country = request.POST.get('country')
        client.state = request.POST.get('state')
        client.save()
        return redirect('my-account')
    return render(request, 'account/change-residence.html', context)


@login_required
def change_address(request):
    client = Account.objects.get(userId=request.user.id)
    address = Address.objects.filter(client__id=request.user.id)
    adresse = 0
    gender = 0
    if address:
        adresse = address[0]
        gender = adresse.gender

    if request.method == 'POST':
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
            client.save()
            return redirect('my-account')
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
            client.save()
            return redirect('my-account')

    context = {'address': adresse, 'gender': gender}
    return render(request, 'account/change-address.html', context)
