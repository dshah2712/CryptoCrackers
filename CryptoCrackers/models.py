from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True)
    id_image = models.ImageField(upload_to='id_images/', null=True, blank=True)

    def __str__(self):
        return self.username
