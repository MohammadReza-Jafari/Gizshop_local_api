import os
import uuid

from django.db import models


def imageSavePath(instance, filename: str):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/products/', filename)


class Color(models.Model):
    name = models.CharField(null=False, max_length=50)
    code = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    perName = models.CharField(null=False, max_length=256)
    engName = models.CharField(max_length=256)
    basePrice = models.FloatField(null=False)
    currentPrice = models.FloatField(null=True)
    brand = models.CharField(max_length=256)
    store = models.CharField(max_length=256)
    rating = models.FloatField(null=True)
    warranty = models.CharField(max_length=256)
    description = models.TextField(null=False)

    # relation
    colors = models.ManyToManyField(Color, null=True, related_name='colors')
    subCategories = models.ManyToManyField(
        'category.SubCategory', null=True, related_name='subCategories'
    )


class Image(models.Model):
    image = models.ImageField(null=True, upload_to=imageSavePath)
    product = models.ForeignKey(Product,related_name='images', on_delete=models.CASCADE, null=False)

