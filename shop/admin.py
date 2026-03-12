from django.contrib import admin
from .models import Product, Order, GalleryImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'featured')
    list_filter = ('category', 'featured')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer_name', 'phone', 'product__name')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'created_at')
    search_fields = ('caption',)
