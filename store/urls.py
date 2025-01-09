from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CollectionViewSet, get_categories, ProductImageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'collections', CollectionViewSet, basename='collections')
router.register(r'product-images', ProductImageViewSet, basename='product-images')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', get_categories, name='get_categories')
]
