from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from . import forms
from . import models


class ReviewListView(generic.ListView):
    template_name = 'review/review_list.html'
    context_object_name = 'latest_review_list'

    def get_queryset(self):
        """
        Return the last nine published reviews (not including those set to be
        published in the future).
        """
        return chain(
            models.InitialReview.objects.filter(
                pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:9],
            models.RewatchReview.objects.filter(
                pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:9],
        )


class MovieListView(generic.ListView):
    template_name = 'review/movie_list.html'
    context_object_name = 'latest_movie_list'

    def get_queryset(self):
        """
        Return the last nine reviewed movies
        """
        return models.Movie.objects.all().order_by('last_reviewed')[:9]


class MovieDetailView(generic.DetailView):
    model = models.Movie
    template_name = 'review/movie_detail.html'


class InitialReviewDetailView(generic.DetailView):
    model = models.InitialReview
    template_name = 'review/initial_review_detail.html'

    def get_queryset(self):
        """
        Excludes any reviews that aren't published yet
        """
        return models.InitialReview.objects.filter(pub_date__lte=timezone.now())


class RewatchReviewDetailView(generic.DetailView):
    model = models.RewatchReview
    template_name = 'review/rewatch_review_detail.html'

    def get_queryset(self):
        """
        Excludes any reviews that aren't published yet
        """
        return models.RewatchReview.objects.filter(pub_date__lte=timezone.now())


@login_required
def add_or_edit_review(request, 
                       movie_id, 
                       initial=True,
                       review_id=None,):
    movie = get_object_or_404(models.Movie, pk=movie_id)
    if initial:
        form_class = forms.InitialReviewForm
        if review_id is not None:
            review = get_object_or_404(models.InitialReview, pk=review_id)
    else:
        form_class = forms.RewatchReviewForm
        if review_id is not None:
            review = get_object_or_404(models.RewatchReview, pk=review_id)
    
    if review_id is not None:
        form = form_class(instance=review)
    else:
        form = form_class()

    if request.method == 'POST':
        if review_id is None:
            form = form_class(request.POST)
        else:
            form = form_class(instance=review, data=request.POST)
        if form.is_valid():
            if review_id is None:
                review = form.save(commit=False)
                review.movie = movie
                review.pub_date = timezone.now()
                review.save()
                messages.success(request, "Added review")
                movie.last_reviewed = timezone.now()
                movie.save()
            else:
                form.save()
                messages.success(request, "Updated review")
            return HttpResponseRedirect(review.get_absolute_url())
    return render(request, 'review/review_form.html', {
        'movie': movie,
        'form': form,
    })


@login_required
def add_or_edit_movie(request, movie_id=None):
    if movie_id is None:
        form = forms.MovieForm()
    else:
        movie = get_object_or_404(models.Movie, pk=movie_id)
        form = forms.MovieForm(instance=movie)

    if request.method == 'POST':
        if movie_id is None:
            form = forms.MovieForm(request.POST)
        else:
            form = forms.MovieForm(instance=movie, data=request.POST)
        if form.is_valid():
            if movie_id is None:
                movie = form.save(commit=False)
                movie.save()
                messages.success(request, "Movie added!")
            else:
                form.save()
                messages.success(request, "Updated {}".format(
                                    form.cleaned_data['title']))
            return HttpResponseRedirect(movie.get_absolute_url())
    return render(request, 'review/movie_form.html', {'form': form,})


def reviews_by_reviewer(request, reviewer):
    reviews = models.InitialReview.objects.filter(reviewer__username=reviewer)
    return render(request, 'review/review_list.html', {'latest_review_list': reviews})


def search(request):
    term = request.GET.get('q')
    reviews = chain(
        models.InitialReview.objects.filter(
            Q(review_text__icontains=term)|Q(watch_for__icontains=term)
        ),
        models.RewatchReview.objects.filter(
            Q(review_text__icontains=term)|Q(discovery__icontains=term)
        ),
    )
    return render(request, 'review/review_list.html', {'latest_review_list': reviews})
