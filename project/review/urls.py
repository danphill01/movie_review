from django.urls import path

from . import views

app_name = 'review'
urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name="review_list"),
    path('movies/', views.MovieListView.as_view(), name="movie_list"),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('movies/<int:movie_id>/comment/', views.comment, name='comment'),
    path('movies/new_movie/', views.new_movie, name='new_movie'),
]
