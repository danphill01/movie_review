from datetime import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
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


class MovieCreateView(generic.CreateView):
    model = models.Movie
    fields = ('imdb_id', 'plot', 'runtime', 'rated', 'title', 'year', 'genre')


class MovieUpdateView(generic.UpdateView):
    model = models.Movie
    fields = ('imdb_id', 'plot', 'runtime', 'rated', 'title', 'year', 'genre')


class MovieDeleteView(generic.DeleteView):
    model = models.Movie
    success_url = reverse_lazy("review:movie_list")


class InitialReviewCreateView(generic.CreateView):
    model = models.InitialReview
    template_name = 'review/review_form.html'
    fields = ('movie', 'review_text', 'watch_for', 'rating', 'pub_date', 'reviewer')

    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = self.kwargs['movie_id']
        initial['reviewer'] = self.request.user.id
        initial['pub_date'] = timezone.now()
        return initial


class InitialReviewUpdateView(generic.UpdateView):
    model = models.InitialReview
    fields = ('movie', 'review_text', 'watch_for', 'rating')
    template_name = 'review/review_form.html'


class InitialReviewDeleteView(generic.DeleteView):
    model = models.InitialReview
    success_url = reverse_lazy("review:review_list")
    template_name = 'review/review_confirm_delete.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(reviewer=self.request.user)
        return self.model.objects.all()


class RewatchReviewCreateView(generic.CreateView):
    model = models.RewatchReview
    template_name = 'review/review_form.html'
    fields = ('movie', 'review_text', 'discovery', 'rating', 'pub_date', 'reviewer')

    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = self.kwargs['movie_id']
        initial['reviewer'] = self.request.user.id
        initial['pub_date'] = timezone.now()
        return initial


class RewatchReviewUpdateView(generic.UpdateView):
    model = models.RewatchReview
    fields = ('movie', 'review_text', 'discovery', 'rating')
    template_name = 'review/review_form.html'


class RewatchReviewDeleteView(generic.DeleteView):
    model = models.RewatchReview
    success_url = reverse_lazy("review:review_list")
    template_name = 'review/review_confirm_delete.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(reviewer=self.request.user)
        return self.model.objects.all()


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
