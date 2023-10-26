from django.contrib import admin
from django.db import models
from .models import UserDetails

# Register your models here.
admin.site.register(UserDetails)