from rest_framework import generics, permissions, authentication,status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from . import serializers, models
from product import models as product_models


class ProductCommentListView(generics.ListAPIView):
    serializer_class = serializers.CommentListSerializer

    def get_queryset(self):
        product = get_object_or_404(product_models.Product, pk=self.kwargs['product_id'])
        return models.Comment.objects\
            .filter(product=product).filter(isAccepted=True).order_by('-createdAt')


class AddCommentView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.CreateCommentSerializer

    def perform_create(self, serializer):
        product = get_object_or_404(product_models.Product, pk=self.kwargs['product_id'])
        serializer.save(user=self.request.user, product=product)


    # admin permissions #

class NotAcceptedCommentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = serializers.CommentListSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(isAccepted=False).order_by('-createdAt')


class AcceptCommentView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=pk)
        comment.isAccepted = True
        comment.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = models.Comment
