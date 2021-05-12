from django.db import models


# Create your models here.


class Tag(models.Model):
    nom = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nom


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    tag = models.ManyToManyField(Tag)
    mainDesc = models.CharField(max_length=2000, null=True)
    mainImg = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg1 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg2 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg3 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg4 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg5 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg6 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg7 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg8 = models.ImageField(upload_to='images/', null=True, blank=True)
    additionalImg9 = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name
