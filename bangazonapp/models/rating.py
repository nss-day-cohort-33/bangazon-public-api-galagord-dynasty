from django.db import models
from .product import Product
from .customer import Customer



class Rating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="ratings")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="ratings")
    rating = models.IntegerField()
    
    

    class Meta:
        verbose_name = ("rating")
        verbose_name_plural = ("ratings")

    