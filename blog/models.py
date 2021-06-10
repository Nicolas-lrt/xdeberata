from django.db import models

# Create your models here.
from django.urls import reverse

from account.models import Account
from ckeditor.fields import RichTextField


class Post(models.Model):
    author = models.ForeignKey(Account, verbose_name='Author of the post', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=40, null=True)
    # body = models.TextField(max_length=3000, null=True)
    body = RichTextField(blank=True, null=True)
    bodyPreview = models.TextField(max_length=500, null=True)
    main_img = models.ImageField(upload_to='images/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_abolute_url(self):
        return reverse('post-list')


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    content = models.TextField(max_length=3000, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return 'Commentaire de \'' + self.name + '\' du poste \'' + self.post.title + '\''