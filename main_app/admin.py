from django.contrib import admin
# import your models here
from .models import Art, Photo

# Register your models here
admin.site.register(Art)
admin.site.register(Photo)
