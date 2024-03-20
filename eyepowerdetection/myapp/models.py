from django.db import models

# Create your models here.

class DataModel(models.Model):
    left=models.CharField(max_length=1000)
    right=models.CharField(max_length=1000)
    both=models.CharField(max_length=1000)
    left_fontsize=models.IntegerField()
    right_fontsize=models.IntegerField()
    both_eye_fontsize=models.IntegerField()
