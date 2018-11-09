from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Movie, Review


class IndexView(generic.ListView):
    template_name = 'review/index.html'
    context_object_name = 'latest_review_list'

    def get_queryset(self):
        """
        Return the last five published reviews (not including those set to be
        published in the future).
        """
        return Review.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'review/movie_detail.html'


class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'review/review_detail.html'

    def get_queryset(self):
        """
        Excludes any reviews that aren't published yet
        """
        return Review.objects.filter(pub_date__lte=timezone.now())


def comment(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.review_set.create(review_text=request.POST['review_text'],
                            rating=request.POST['rating'],
                            pub_date=timezone.now(),
                            )
    return HttpResponseRedirect(reverse('review:index'))

