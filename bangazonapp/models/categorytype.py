from django.db import models


class CategoryType(models.Model):

    name = models.CharField(max_length=50)
    
    

    class Meta:
        verbose_name = ("categorytype")
        verbose_name_plural = ("categorytypes")

    def __str__(self):
        return self.name