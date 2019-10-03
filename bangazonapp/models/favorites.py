from django.db import models
from .customer import Customer


class Favorite(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="favorites")
    seller = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="favorites")
    
    

    class Meta:
        verbose_name = ("favorite")
        verbose_name_plural = ("favorites")
