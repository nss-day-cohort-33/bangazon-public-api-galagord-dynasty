from django.db import models
from .product import Product
from .order import Order


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderproducts")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="orderproducts")
    
    
    
    

    class Meta:
        verbose_name = ("order product")
        verbose_name_plural = ("order products")