from django.urls import path
from . import views


urlpatterns = [
    path('logout', views.logoutUser, name='logout'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('login', views.loginPage, name='login'),
    path('my-account', views.my_account, name='my-account'),
    path('change-last-name', views.change_last_name, name='change-last-name'),
    path('change-first-name', views.change_first_name, name='change-first-name'),
    path('change-email', views.change_email, name='change-email'),
    path('change-password', views.change_password, name='change-password'),
]
