from rest_framework import serializers

from . import models


class MainCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MainCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'
        depth = 1


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategory
        fields = '__all__'


class SubCategoryReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategory
        fields = '__all__'
        depth = 2


class CategoryNestedSerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = models.Category
        fields = ('id', 'title', 'sub_categories')


class MainCategoryListSerializer(serializers.ModelSerializer):
    categories = CategoryNestedSerializer(many=True)

    class Meta:
        model = models.MainCategory
        fields = ('id', 'title', 'categories')
