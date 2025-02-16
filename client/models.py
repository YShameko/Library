from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    role = models.TextField()
    home_address = models.TextField(default="client")
    phone_numer = models.TextField()  # models.PhoneNumberField()
    gender = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)