from django.db import models
from django.utils import timezone
from .customer import Customer
from .categorytype import CategoryType
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class Product(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    location = models.CharField(max_length=50)
    image = models.ImageField(upload_to=".static/media", blank=True)
    category_type = models.ForeignKey(CategoryType, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)


    @property
    def total_sold(self):
        return self.orderproduct_set.filter(order__payment__isnull=False).count()


    class Meta:
        verbose_name = ("product")
        verbose_name_plural = ("products")

    def __str__(self):
        return self.name
