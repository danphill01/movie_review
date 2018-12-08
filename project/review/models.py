import datetime

from django.db import models
from django.utils import timezone


class Movie(models.Model):
    imdb_id = models.CharField(max_length=10)
    plot = models.TextField(default='')
    runtime = models.CharField(max_length=10)
    rated = models.CharField(max_length=10)
    title = models.CharField(max_length=80)
    year = models.IntegerField(default=1900)
    last_reviewed = models.DateTimeField('last reviewed')

    def __str__(self):
        return '{} - {} ({})'.format(self.title, self.rated, self.year)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=200)
    rating = models.IntegerField(default = 0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return '{}: {} - {}'.format(self.movie, self.review_text, self.pub_date.strftime("%I:%M%p %d%b%Y"))

    def was_published_recently(self):
        now = timezone.now() 
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 


