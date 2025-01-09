from django.contrib import admin
from .models import Product, Collection, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    readonly_fields = ('image', 'product')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image}" width="100 height="100" style="object-fit: contain;"/>'
        return 'No Image'
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'category', 'price', 'stock', 'get_images', 'created_at')
    search_fields = ('name','collection', 'category')
    list_editable = ['category', 'collection', 'stock']
    list_filter = ('created_at',)
    inlines = [ProductImageInline]

    def get_images(self, obj):
        images = obj.images.all()
        if images:
            return ", ".join([str(image.image.url.split('/')[-1] for image in images)])
        return 'No Images'
    get_images.short_description = 'Associated Images'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creative', 'cover_img', 'created_at')  # Columns to display in the list view
    search_fields = ('name','creative')                                # Add a search box for 'name'
    list_filter = ('created_at',)