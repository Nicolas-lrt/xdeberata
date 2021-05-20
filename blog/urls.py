from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('mini', views.miniindex, name='minihome'),
    path('404', views.error404page, name='error404'),
    path('about', views.aboutPage, name='aboutPage'),
]
