from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_shop, name='home-shop'),
    path('delete-prod/<str:pk>', views.delete_product, name='delete-product'),

]
