from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from account.decorators import unauthenticated_user
from account.forms import CreateAccount
from account.models import Account


def logoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def sign_in(request):
    form = CreateAccount()
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            user = form.save()
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
