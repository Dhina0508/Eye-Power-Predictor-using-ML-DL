from django.db import models

# Create your models here.

class DataModel(models.Model):
    image=models.CharField(max_length=1000)
    fontSize=models.IntegerField()
