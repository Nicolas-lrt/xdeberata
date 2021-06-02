from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('mini', views.miniindex, name='minihome'),
    path('404', views.error404page, name='error404'),
    path('about', views.aboutPage, name='aboutPage'),
    path('post/<slug:slug>', views.postPage, name='post_detail'),
    path('post-list', views.postList, name='post-list'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)