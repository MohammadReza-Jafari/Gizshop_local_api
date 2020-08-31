import os

from rest_framework import generics, permissions, authentication, status, filters
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from core.permissions import IsAdmin
from . import serializers
from . import models


class GetAllProductView(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('perName', 'engName', 'brand', 'warranty')
    ordering_fields = ('currentPrice', 'rating')

    def get_queryset(self):
        amazing = bool(self.request.query_params.get('amazing', None))

        if amazing:
            return models.Product.objects.filter(amazing=True)

        return models.Product.objects.order_by('pk').all()


class GetProductByMainCategory(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('perName', 'engName', 'brand', 'warranty')
    ordering_fields = ('currentPrice', 'rating')

    def get_queryset(self):
        return models.Product.objects.filter(
            subCategory__category__main_category_id=self.kwargs['main_category_id']
        )


class GetProductByCategory(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('perName', 'engName', 'brand', 'warranty')
    ordering_fields = ('currentPrice', 'rating')

    def get_queryset(self):
        return models.Product.objects.filter(
            subCategory__category_id=self.kwargs['category_id']
        )


class GetProductBySubCategory(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('perName', 'engName', 'brand', 'warranty')
    ordering_fields = ('currentPrice', 'rating')

    def get_queryset(self):
        return models.Product.objects.filter(
            subCategory_id=self.kwargs['sub_category_id']
        )


class GetProductView(generics.RetrieveAPIView):
    serializer_class = serializers.SingleProductSerializer

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


class GetProductPriceView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(models.Product, pk=pk)
        return Response(
            {'basePrice': product.basePrice, 'currentPrice': product.currentPrice},
            status=status.HTTP_200_OK
        )


class AddToAmazingOffer(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, pk, *args, **kwargs):
        amazing_offers = models.Product.objects.filter(amazing=True)
        if len(amazing_offers) == 15:
            return Response(
                {'error': "تعداد کالاهای شگفت انگیز به حد نصاب (15) رسیده است"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        product = get_object_or_404(models.Product, pk=pk)

        try:
            discount = int(request.data['discountPercent'])
        except ValueError as e:
            return Response({'error': 'درصد تخفیف باید عدد باشد'}, status=status.HTTP_400_BAD_REQUEST)

        if not 0 < discount < 51:
            return Response(
                {'error': "درصد تخفیف باید بین 0 تا 50 باشد"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.amazing = True
        product.discountPercent = discount
        product.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


class DeleteFromAmazingOffers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(models.Product, pk=pk)
        product.discountPercent = 0
        product.amazing = False
        product.save()

        return Response({'result': 'success'}, status=status.HTTP_200_OK)