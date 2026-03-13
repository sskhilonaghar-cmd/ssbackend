from rest_framework import serializers
from .models import Product, Order, GalleryImage


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="image.url", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="image.url", read_only=True)

    class Meta:
        model = GalleryImage
        fields = "__all__"
