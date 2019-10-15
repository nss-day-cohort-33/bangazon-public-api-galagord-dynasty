from django.db import models
from .customer import Customer
from django.urls import reverse
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class Payment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=50)
    account_number = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payment")


    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")

    def __str__(self):
        return self.merchant_name