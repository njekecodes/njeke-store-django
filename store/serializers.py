from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Collection, ProductImage


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'creative', 'cover_img', 'is_released', ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'collection', 'category', 'price', 'stock', 'description', 'images']

    def get_images(self, obj):
        return[
            {'id': image.id, 'image': image.image.url}
            for image in obj.productimage_set.all()
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_staff']
