from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Product, ProductImage
from .serializers import ProductSerializer


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
        return Response(product_serializer.erros, status=status.HTTP_400_BAD_REQUEST)