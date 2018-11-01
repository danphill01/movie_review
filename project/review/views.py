from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

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


def comment(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.review_set.create(review_text=request.POST['review_text'],
                            rating=request.POST['rating'],
                            pub_date=timezone.now(),
                            )
    return HttpResponseRedirect(reverse('review:index'))

