from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Movie, Review


def index(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:5]
    context = {
        'latest_review_list': latest_review_list,
    }
    return render(request, 'review/index.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'review/movie_detail.html', {'movie': movie})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review/review_detail.html', {'review': review})


def movie_reviews(request, movie_id):
    response = "You're looking at the reviews of movie %s."
    return HttpResponse(response % movie_id)


def comment(request, movie_id):
    return HttpResponse("You're leaving a review of movie %s." % movie_id)


