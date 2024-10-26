from django.contrib import admin
from .models import Product, Collection


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'price', 'stock', 'created_at')  # Columns to display in the list view
    search_fields = ('name','collection')                                # Add a search box for 'name'
    list_filter = ('created_at',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creative', 'cover_img', 'created_at')  # Columns to display in the list view
    search_fields = ('name','creative')                                # Add a search box for 'name'
    list_filter = ('created_at',)