from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Collection, ProductImage
from .serializers import ProductSerializer, CollectionSerializer, ProductImageSerializer
from .utils import load_json_data


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class =  ProductImageSerializer

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

    def create(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product = product_serializer.save()

            # Handle product images
            images = request.FILES.getlist('images')
            for image in images:
                product_image = ProductImage(product=product, src=image)
                product_image.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    filterable_fields = ['collection', 'category']

    def search_products(self):
        queryset = super().get_queryset()

        for field in self.filterable_fields:
            filter_value = self.request.query_params.get(field)
            if filter_value:
                queryset = queryset.filter(**{field: filter_value})

            return queryset


@api_view(['GET'])
def get_categories(request):
    categories = load_json_data('categories.json')
    return Response(categories)