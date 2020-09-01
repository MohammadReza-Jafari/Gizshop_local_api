from rest_framework import generics, permissions, authentication, status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from . import serializers, models
from user.models import CustomUser
from product.models import Product


class GetAllCaretView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.CartListSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(buyer=self.request.user)


class GetSingleCaretView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.SingleCartSerializer

    def get_object(self):
        cart = get_object_or_404(models.Cart, buyer=self.request.user, pk=self.kwargs['pk'])
        return cart


class AddToCaretView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, product_id):
        user: CustomUser = request.user
        product = get_object_or_404(Product, pk=product_id)
        carts = user.carts
        if carts.filter(is_paid=False).exists():
            cart = carts.get(is_paid=False)
            cart_items = cart.cart_items
            if cart_items.filter(product=product).exists():
                item = cart_items.get(product=product)
                item.number += 1
                if product.amazing:
                    cart.total_amount += int(product.basePrice * product.discountPercent)
                cart.total_amount += product.currentPrice
                item.save()
                cart.save()
                return Response({'result': 'کالا با موفقیت اضافه شد'}, status=status.HTTP_200_OK)

            cart_items.create(product=product, number=1)
            if product.amazing:
                cart.total_amount += int(product.basePrice * product.discountPercent)
            cart.total_amount += product.currentPrice
            cart.save()
            return Response({'result': 'کالا با موفقیت اضافه شد'}, status=status.HTTP_200_OK)

        cart = carts.create(total_amount=0, is_paid=False)
        if product.amazing:
            cart.total_amount += int(product.basePrice * product.discountPercent)
        cart.total_amount += product.currentPrice
        cart.cart_items.create(product=product, number=1)
        cart.save()
        return Response({'result': 'کالا با موفقیت اضافه شد'}, status=status.HTTP_200_OK)
