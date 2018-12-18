import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User


class Movie(models.Model):
    imdb_id = models.CharField(max_length=10)
    plot = models.TextField(default='')
    runtime = models.CharField(max_length=10)
    rated = models.CharField(max_length=10)
    title = models.CharField(max_length=80)
    year = models.IntegerField(default=1900)
    last_reviewed = models.DateTimeField('last reviewed', blank=True, null=True)
    genre = models.CharField(default='', max_length=100)

    def __str__(self):
        return '{} - {} ({})'.format(self.title, self.rated, self.year)

    def get_absolute_url(self):
        return reverse('review:movie_detail', kwargs={'pk': self.id})

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(default = 0)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}: {} - {}'.format(self.movie, self.review_text, self.pub_date.strftime("%I:%M%p %d%b%Y"))

    def was_published_recently(self):
        now = timezone.now() 
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 


class InitialReview(Review):
    watch_for = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('review:initial_review_detail', kwargs={
                         'pk': self.id}
                      )


class RewatchReview(Review):
    discovery = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('review:rewatch_review_detail', kwargs={
                         'pk': self.id}
                      )
