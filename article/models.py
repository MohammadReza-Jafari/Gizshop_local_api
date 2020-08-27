from django.db import models


class Vote(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    choice = models.BooleanField(null=False)


class Article(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=500, null=False, default='')
    body = models.TextField(null=False)
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='articles')
    createdAt = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(Vote, related_name='votes')
