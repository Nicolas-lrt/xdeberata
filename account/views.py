from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from account.decorators import unauthenticated_user, admin_only
from account.forms import CreateAccount
from account.models import Account


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
            account = Account(user_id=user.id)
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
    return render(request, 'account/my-account.html')


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


