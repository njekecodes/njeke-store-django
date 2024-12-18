from django.contrib import admin
from .models import Product, Collection, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'category', 'price', 'stock', 'created_at')  # Columns to display in the list view
    search_fields = ('name','collection', 'category')                                # Add a search box for 'name'
    list_editable = ['category', 'collection', 'stock']
    list_filter = ('created_at',)
    inlines = [ProductImageInline]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creative', 'cover_img', 'created_at')  # Columns to display in the list view
    search_fields = ('name','creative')                                # Add a search box for 'name'
    list_filter = ('created_at',)