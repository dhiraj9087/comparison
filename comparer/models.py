from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    delivery_time = models.CharField(max_length=50)
    warranty = models.CharField(max_length=50)

    def __str__(self):
        return self.name