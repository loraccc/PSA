from django.contrib import admin
from .models import AppUser,Item
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Item)