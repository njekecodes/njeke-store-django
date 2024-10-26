from django import forms
from django.forms import modelformset_factory

from backend.store.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'collection', 'price', 'stock', 'description']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        field = ['src']

ProductImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)

