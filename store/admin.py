from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'created_at')  # Columns to display in the list view
    search_fields = ('title',)                                # Add a search box for 'name'
    list_filter = ('created_at',)