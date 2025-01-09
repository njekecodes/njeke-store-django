import os

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Collection, ProductImage
from .serializers import ProductSerializer, CollectionSerializer, ProductImageSerializer, UserSerializer
from .utils import load_json_data


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.all()

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')

        if not product_id:
            return Response({'error': 'Product is required!'}, status=status.HTTP_400_BAD_REQUEST)

        image_count = ProductImage.objects.filter(product_id=product_id).count()
        if image_count >= 5:
            return Response(
                {'error': 'Maximum of 5 images per product allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterable_fields = ['id', 'collection', 'category']

    def create(self, request, *args, **kwargs):
        data = request.data

        # validate collection
        collection_id = data.get('collection')
        try:
            collection = Collection.objects.get(id=collection_id)
        except Collection.DoesNotExist:
            return Response({'error': 'Invalid collection'}, status=status.HTTP_400_BAD_REQUEST)

        # create product
        product = Product.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            category=data.get('category'),
            collection_id=data.get('collection'),
            stock=data.get('stock'),
        )
        # Handle product images
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                file_name = image.name
                ProductImage.objects.create(product=product, image=file_name)

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = super().get_queryset()

        for field in self.filterable_fields:
            filter_value = self.request.query_params.get(field)
            if filter_value:
                if field == 'collection':
                    try:
                        collection = Collection.objects.get(name__iexact=filter_value)
                        queryset = queryset.filter(collection=collection.id)
                    except Collection.DoesNotExist:
                        return queryset.none()
                elif field == 'id':
                    queryset = queryset.filter(id=filter_value).first()
                    print('Product Found')

                else:
                    queryset = queryset.filter(**{f'{field}__iexact': filter_value})

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def get_categories(request):
    categories = load_json_data('categories.json')
    return Response(categories)
