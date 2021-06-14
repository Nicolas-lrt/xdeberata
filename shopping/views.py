from django.shortcuts import render

# Create your views here.


def home_shop(request):
    return render(request, 'shopping/home-shop.html')
