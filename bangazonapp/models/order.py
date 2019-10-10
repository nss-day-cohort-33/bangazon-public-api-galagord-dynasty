from django.db import models
from .customer import Customer
from .payment import Payment


class Order(models.Model):

    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="payment")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customer")
    created_date = models.DateField(auto_now_add=True)
    line_items = models.ManyToManyField("Product", through="OrderProduct")

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")
