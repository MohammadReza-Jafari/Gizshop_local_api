from rest_framework import serializers

from . import models
from product.models import Product


class CartListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = models.Cart
        fields = '__all__'


class ProductInCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'perName', 'engName')


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInCartItemSerializer()

    class Meta:
        model = models.CartItem
        fields = ('id', 'product', 'number')


class SingleCartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = models.Cart
        fields = ('cart_items', 'total_amount', 'created_date', 'is_paid', 'user')
