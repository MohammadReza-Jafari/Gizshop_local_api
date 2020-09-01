from django.db import models


class Cart(models.Model):
    buyer = models.ForeignKey(
        'user.CustomUser', on_delete=models.CASCADE, related_name='carts', null=False
    )
    is_paid = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(default=0)


class CartItem(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')

