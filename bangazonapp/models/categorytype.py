from django.db import models


class CategoryType(models.Model):

    name = models.CharField(max_length=50)
    
    

    class Meta:
        verbose_name = ("category type")
        verbose_name_plural = ("category types")

    def __str__(self):
        return self.name