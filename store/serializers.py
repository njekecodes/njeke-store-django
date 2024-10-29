from rest_framework import serializers
from .models import Product, Collection, ProductImage


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()

    class Meta:
        model = Product
        fields = '__all__'

