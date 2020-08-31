from rest_framework import serializers

from django.shortcuts import get_object_or_404

from . import models
from category import serializers as category_serializers
from category import models as category_models


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Color
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'


class SingleProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)
    subCategory = category_serializers.SubCategoryReadSerializer(read_only=False)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'perName', 'engName', 'basePrice', 'currentPrice', 'brand', 'store',
            'rating', 'warranty', 'amazing', 'discountPercent', 'description', 'colors',
            'subCategory', 'images'
        )


class ListProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'perName', 'engName', 'basePrice', 'currentPrice',
            'amazing', 'discountPercent', 'store', 'rating', 'images'
        )


class EditProductSerializer(serializers.ModelSerializer):
    colors = serializers.PrimaryKeyRelatedField(
        queryset=models.Color.objects.all(),
        many=True
    )
    subCategory = serializers.PrimaryKeyRelatedField(
        queryset=category_models.SubCategory.objects.all(),
    )
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'perName', 'engName', 'basePrice', 'currentPrice', 'brand', 'store',
            'rating', 'warranty', 'description', 'colors', 'subCategory', 'images'
        )


class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    class Meta:
        fields = ('image',)

    def create(self, validated_data):
        product = get_object_or_404(models.Product, pk=self.context['view'].kwargs['product_id'])
        image = models.Image.objects.create(image=validated_data['image'], product=product)
        return image
