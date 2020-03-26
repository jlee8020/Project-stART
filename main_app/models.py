from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
import datetime
from phonenumber_field.modelfields import PhoneNumberField

PRESENT = (
    ('Yes', 'Yes'),
    ('At Risk', 'At Risk'),
    ('No', 'No')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class ProfilePhoto(models.Model):
    url = models.CharField(max_length=200)
    filename = models.CharField(max_length=50)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Art(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.CharField(
        max_length=7,
        choices=PRESENT,
        default=PRESENT[0][0]
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('art_detail', kwargs={'art_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    filename = models.CharField(max_length=50)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    content = models.TextField(max_length=200)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # change the default sort for comments
    class Meta:
        ordering = ['-date']