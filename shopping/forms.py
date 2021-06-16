from django import forms
from .models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
                    'name',
                    'price',
                    'mainDesc',
                    'shortDesc',
                    'mainImg',
                    'additionalImg1',
                    'additionalImg2',
                    'additionalImg3',
                    'additionalImg4',
                    'additionalImg5',
                    'additionalImg6',
                    'additionalImg7',
                    'additionalImg8',
                    'additionalImg9'
              ]
