from django import forms
from .models import Product, Tag


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'tag',
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
            'additionalImg9',
        ]

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )