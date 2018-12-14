from django import forms

from . import models


class MovieForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = [
           'imdb_id',
           'plot',
           'runtime',
           'rated',
           'title',
           'year',
        ]
        exclude = [
            'last_reviewed',
        ]


class InitialReviewForm(forms.ModelForm):
    class Meta:
        model = models.InitialReview
        fields = [
            'review_text',
            'rating',
            'watch_for',
        ]



class RewatchReviewForm(forms.ModelForm):
    class Meta:
        model = models.RewatchReview
        fields = [
            'review_text',
            'rating',
            'discovery',
        ]


