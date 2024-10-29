from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CollectionViewSet, get_categories

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'collections', CollectionViewSet, basename='collections')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', get_categories, name='get_categories')
]
