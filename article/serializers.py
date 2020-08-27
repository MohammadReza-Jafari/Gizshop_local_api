from rest_framework import serializers

from . import models


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = models.Article
        fields = '__all__'


class ListArticleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = ('id', 'title', 'description', 'author', 'createdAt', 'likes', 'dislikes')

    def get_likes(self, obj):
        return len(obj.votes.filter(choice=True))

    def get_dislikes(self, obj):
        return len(obj.votes.filter(choice=False))


class CreateOrEditArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = ('title', 'body', 'description')
