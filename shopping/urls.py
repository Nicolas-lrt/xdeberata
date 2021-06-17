from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_shop, name='home-shop'),
    path('delete-prod/<str:pk>', views.delete_product, name='delete-product'),
    path('add-product', views.AddProduct.as_view(), name='add-product')

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)