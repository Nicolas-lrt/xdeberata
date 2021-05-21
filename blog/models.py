from django.db import models

# Create your models here.
from account.models import Account


class Post(models.Model):
    author = models.ForeignKey(Account, verbose_name='Author of the post', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    field = models.TextField(max_length=3000)
