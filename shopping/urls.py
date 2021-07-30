from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path


urlpatterns = [
    path('', views.home_shop, name='home-shop'),
    path('search', views.shop_search, name='shop-search'),
    path('delete-prod/<str:pk>', views.delete_product, name='delete-product'),
    path('add-product', views.AddProduct.as_view(), name='add-product'),
    path('product/<str:pk>', views.product_detail, name='product-detail'),
    path('update-product/<str:pk>', views.UpdateProductView.as_view(), name='update-product'),
    path('add-to-cart/<str:pk><str:qty>', views.addToCart, name='addToCart'),
    path('clear-cartLine/<str:pk>', views.clearCartLine, name='clear-cart-line'),
    path('remove-from-cart/<str:pk>', views.removeFromCart, name='remove-from-cart'),
    path('clear-cart/', views.clearCart, name='clear-cart'),
    path('cart/', views.cartPage, name='cart-page'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('create-order/', views.createOrder),
    path('orders', views.orderPage, name='orders-page'),
    path('order-detail/<str:pk>/', views.orderDetails, name='orderDetail'),
    path('order-list', views.order_list, name='order-list'),
    path('order-list-search', views.order_list_search, name='order-list-search'),
    path('order-list-search-id', views.order_list_search_id, name='order-list-search-id'),
    path('change-order-status/<str:order_id>/<str:pk>', views.change_order_state, name='change-order-status'),
    path('choose-address', views.choose_address, name='choose-address'),
    path('choose-invoice', views.choose_invoice, name='choose-invoice'),
    path('cart-recap', views.cart_recap, name='cart-recap'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)