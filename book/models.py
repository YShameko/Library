import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Authors(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    rating = models.FloatField(default=5)

    def __str__(self):
        return self.name

class Genres(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=5)

    def __str__(self):
        return self.name

class Publishers(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=5)

    def __str__(self):
        return self.name

class Books(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    publish_year = models.IntegerField()
    reception_date = models.DateField()
    cover = models.ImageField(upload_to='covers/')
    rating = models.FloatField(default=5)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    rating = models.FloatField(default=5)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)

class Borrowed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    closed = models.BooleanField(default=False)
    ready_to_return = models.BooleanField(default=False)
    comments = models.CharField(max_length=500)
