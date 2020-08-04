from django.db import models


class Comment(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(null=False)
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    isAccepted = models.BooleanField(default=False)
