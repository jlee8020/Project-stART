from django.db import models

# Create your models here.

class Art(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    yearCreated = models.IntegerField()

class Photo(models.Model):
  url = models.CharField(max_length=200)
  art = models.ForeignKey(Art, on_delete=models.CASCADE)
