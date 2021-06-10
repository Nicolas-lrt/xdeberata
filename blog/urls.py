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
    path('add-post', views.add_post, name='add-post'),
    path('delete-p/<str:pk>', views.delete_post, name='delete-post'),
    path('delete-c/<str:pk>', views.delete_comment, name='delete-comment'),
    path('update-post/<str:pk>', views.UpdatePostView.as_view(), name='update-post'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)