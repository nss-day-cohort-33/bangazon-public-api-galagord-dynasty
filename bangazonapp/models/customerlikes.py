from django.db import models
from .customer import Customer
from .product import Product


class CustomerLikes(models.Model):

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="customerlikes")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customerlikes")
    is_liked = models.BooleanField()
    
    

    class Meta:
        verbose_name = ("customer like")
        verbose_name_plural = ("customer likes")