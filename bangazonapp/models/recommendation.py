from django.db import models
from .customer import Customer
from .product import Product


class Recommendation(models.Model):

    receive_customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="recommendations")
    send_customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="recommendations")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="recommendations")
    
    

    class Meta:
        verbose_name = ("recommendation")
        verbose_name_plural = ("recommendations")