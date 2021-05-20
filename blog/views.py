from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def miniindex(request):
    return render(request, 'home-minimal.html')


def error404page(request):
    return render(request, '404-error.html')


def aboutPage(request):
    return render(request, 'about.html')
