from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = CountryField(blank_label='(Select country)', blank=True, null=True)
    county = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"