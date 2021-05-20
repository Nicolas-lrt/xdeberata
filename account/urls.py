from django.urls import path
from . import views


urlpatterns = [
    path('logout', views.logoutUser, name='logout'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('login', views.loginPage, name='login'),
]
