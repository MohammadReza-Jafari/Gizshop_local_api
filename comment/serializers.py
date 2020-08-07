from rest_framework import serializers

from . import models


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('title', 'text', )


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = models.Comment
        fields = ('id', 'title', 'text', 'user', 'product', 'createdAt')
