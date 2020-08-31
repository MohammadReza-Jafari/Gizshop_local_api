from rest_framework import generics, permissions, authentication

from . import serializers
from . import models
from core.permissions import IsAdmin


class GetAllCategoriesView(generics.ListAPIView):
    serializer_class = serializers.MainCategoryListSerializer
    queryset = models.MainCategory.objects.all().order_by('id')


class CreateMainCategoryView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.MainCategorySerializer


class MainCategoryListView(generics.ListAPIView):
    queryset = models.MainCategory.objects.all()
    serializer_class = serializers.MainCategorySerializer


class ManageMainCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MainCategory.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.MainCategorySerializer


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.CategoryNestedSerializer


class MangeCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)


class CreateSubCategoryView(generics.CreateAPIView):
    serializer_class = serializers.SubCategorySerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)


class SubCategoryListView(generics.ListAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategoryReadSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


class MangeSubCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)
