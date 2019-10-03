from django.db import models
from .customer import Customer
from .payment import Payment


class Order(models.Model):

    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name="orders")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="orders")
    created_date = models.DateField(auto_now_add=True)
    
    
    

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")