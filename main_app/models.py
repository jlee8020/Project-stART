from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Art(models.Model):
  name = models.CharField(max_length=100)
  artist = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  yearCreated = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Photo(models.Model):
  url = models.CharField(max_length=200)
  art = models.ForeignKey(Art, on_delete=models.CASCADE)

