from rest_framework import generics, permissions, authentication, status, filters
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from . import serializers, models
from core import permissions as custom_permissions


class ListArticleView(generics.ListAPIView):
    serializer_class = serializers.ListArticleSerializer
    queryset = models.Article.objects.all().order_by('-createdAt')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', 'body')


class SingleArticleView(generics.RetrieveAPIView):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.all()


class VoteArticleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=pk)
        vote = request.query_params.get('vote', None)
        if not vote:
            return Response({'error': 'درخواست معتبر نمی باشد.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            vote = bool(vote)

        if vote:
            if len(article.votes.filter(user=request.user)) > 0:
                return Response(
                    {'error': 'شما قبلا به این مقاله رای داده اید.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            article.votes.create(user=request.user, choice=vote)
            article.save()
            return Response({'result': 'success'})


# admin permissions

class CreateArticleView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.CreateOrEditArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ManageArticleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, custom_permissions.IsBossOrOwner)
    serializer_class = serializers.CreateOrEditArticleSerializer
