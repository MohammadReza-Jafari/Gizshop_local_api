import os

from rest_framework import generics, permissions, authentication, status, filters
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from core.permissions import IsAdmin
from . import serializers
from . import models


class GetAllProductView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ShowProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('perName', 'engName', 'brand', 'warranty')
    ordering_fields = ('currentPrice', 'rating')


class GetProductView(generics.RetrieveAPIView):
    serializer_class = serializers.ShowProductSerializer

    def get_object(self):
        return get_object_or_404(models.Product, pk=self.kwargs['pk'])


# admin permissions #

class CreateProductView(APIView):
    permission_classes = (IsAdmin,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        images = request.data.pop('images')
        ser = serializers.ProductSerializer(data=request.data)

        if ser.is_valid():
            colors = ser.validated_data.pop('colors')
            sub_categories = ser.validated_data.pop('subCategories')
            product = models.Product.objects.create(**ser.validated_data)

            for image in images:
                image_dict = {
                    'image': image,
                    'product': product.id
                }
                image_ser = serializers.ImageSerializer(data=image_dict)
                if image_ser.is_valid():
                    img = models.Image.objects.create(**image_ser.validated_data)
                    img.save()
                else:
                    return Response(
                        {'error': 'select a valid image'}, status=status.HTTP_400_BAD_REQUEST
                    )
            product.save()
            product.colors.set(colors)
            product.subCategories.set(sub_categories)
            return Response({'result': 'success'}, status=status.HTTP_201_CREATED)
        return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProductView(generics.RetrieveUpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.EditProductSerializer

    def get_object(self):
        return get_object_or_404(models.Product, pk=self.kwargs['pk'])


class DeleteProductView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(models.Product, pk=self.kwargs['pk'])
        images = models.Image.objects.filter(product=product)
        for image in images:
            path = image.image.path
            if os.path.exists(path):
                os.remove(path)
        product.delete()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


class AddImageToProductView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.ImageInputSerializer


class DeleteProductImageView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, img_id, *args, **kwargs):
        image = get_object_or_404(models.Image, pk=img_id)
        if os.path.exists(image.image.path):
            os.remove(image.image.path)
            image.delete()
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Image Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
