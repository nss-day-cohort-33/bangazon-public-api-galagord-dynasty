from django.db import models
from .product import Product
from .order import Order


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="cart")

    class Meta:
        verbose_name = ("line_item")
        verbose_name_plural = ("line_items")
