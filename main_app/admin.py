from django.contrib import admin
# import your models here
from .models import Art, Photo, Comment, Profile, ProfilePhoto

# Register your models here
admin.site.register(Art)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(ProfilePhoto)
