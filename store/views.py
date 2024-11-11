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
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product = product_serializer.save()

            # Handle product images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        return self.queryset


    def search_products(self):
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
                    filter_key = f'{field}__iexact'
                    queryset = queryset.filter(**{f'{field}__iexact': filter_value})

        return queryset


@api_view(['GET'])
def get_categories(request):
    categories = load_json_data('categories.json')
    return Response(categories)
