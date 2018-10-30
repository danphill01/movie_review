import datetime

from django.db import models
from django.utils import timezone


class Movie(models.Model):
    imdb_id = models.TextField(default='')
    plot = models.TextField(default='')
    runtime = models.TextField(default='')
    rated = models.TextField(default='Unknown')
    title = models.TextField(default='')
    year = models.IntegerField(default=1900)

    def __str__(self):
        return self.title


class Firstview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    firstview_text = models.CharField(max_length=200)
    rating = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.firstview_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=200)
    rating = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.review_text


