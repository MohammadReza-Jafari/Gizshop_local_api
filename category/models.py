from django.db import models


class MainCategory(models.Model):
    title = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(null=False, max_length=256)
    main_category = models.ForeignKey(
        MainCategory,
        related_name='categories',
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(null=False, max_length=256)
    category = models.ForeignKey(
        Category, related_name='sub_categories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
