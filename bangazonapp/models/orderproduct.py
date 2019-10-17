
from django.db import models
from .product import Product
from .order import Order


class OrderProduct(models.Model):

    # orderproduct_set is default related name. If this model had a related name, that is what you would use instead of orderproduct set. See product model for example.

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("line_item")
        verbose_name_plural = ("line_items")