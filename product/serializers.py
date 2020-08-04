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


class ShowProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)
    subCategories = category_serializers.SubCategorySerializer(many=True, read_only=False)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'perName', 'engName', 'basePrice', 'currentPrice', 'brand', 'store',
            'rating', 'warranty', 'description', 'colors', 'subCategories', 'images'
        )


class EditProductSerializer(serializers.ModelSerializer):
    colors = serializers.PrimaryKeyRelatedField(
        queryset=models.Color.objects.all(),
        many=True
    )
    subCategories = serializers.PrimaryKeyRelatedField(
        queryset=category_models.SubCategory.objects.all(),
        many=True
    )
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            'id', 'perName', 'engName', 'basePrice', 'currentPrice', 'brand', 'store',
            'rating', 'warranty', 'description', 'colors', 'subCategories', 'images'
        )


class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    class Meta:
        fields = ('image',)

    def create(self, validated_data):
        product = get_object_or_404(models.Product, pk=self.context['view'].kwargs['product_id'])
        image = models.Image.objects.create(image=validated_data['image'], product=product)
        return image
