from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from shopping.models import Product


class Account(models.Model):
    user = models.ForeignKey(User, verbose_name='Associated user', on_delete=models.CASCADE)
    userId = models.IntegerField(null=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class CartLine(models.Model):
    """
    Une ligne de panier client.
    """
    client = models.ForeignKey(Account, verbose_name='Associated user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'User cart line'
        verbose_name_plural = 'User cart lines'

    def total(self):
        return round(self.product.price * float(self.quantity), 2)

    def __str__(self):
        return '\'' + self.client.user.username + '\' user cart line'
