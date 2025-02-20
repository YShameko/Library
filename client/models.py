from django.db import models
from django.contrib.auth.models import User
from book.models import Authors, Genres

# Create your models here.
class UserProfile(models.Model):
    home_address = models.TextField(default="client")
    phone = models.TextField()  # models.PhoneNumberField()
    personal_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # role = models.TextField()

class FavAuthors(models.Model):
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FavGenres(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)