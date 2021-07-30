from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
from django.urls import reverse
from slugify import slugify


class Tag(models.Model):
    nom = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nom


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug_prod = models.SlugField(max_length=40, null=True)
    price = models.FloatField(null=True,  validators=[MinValueValidator(0.0)])
    tag = models.ManyToManyField(Tag)
    mainDesc = RichTextField(blank=True, null=True)
    shortDesc = models.TextField(max_length=255, null=True)
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

    def setSlug(self):
        self.slug = slugify(self.name)

    def get_absolute_url(self):
        return reverse('home-shop')
