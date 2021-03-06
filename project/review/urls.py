from django.urls import path

from . import views

app_name = 'review'
urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name="review_list"),
    path('movies/', views.MovieListView.as_view(), name="movie_list"),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('reviews/i<int:pk>/', views.InitialReviewDetailView.as_view(), name='initial_review_detail'),
    path('reviews/r<int:pk>/', views.RewatchReviewDetailView.as_view(), name='rewatch_review_detail'),
    path('movies/<int:movie_id>/new_initial_review/', views.InitialReviewCreateView.as_view(), name='add_initial_review'),
    path('movies/<int:movie_id>/new_rewatch_review/', views.RewatchReviewCreateView.as_view(), name='add_rewatch_review'),
    path('movies/new_movie/', views.MovieCreateView.as_view(), name='new_movie'),
    path('movies/edit_movie/<int:pk>/', views.MovieUpdateView.as_view(), name='edit_movie'),
    path('movies/delete_movie/<int:pk>/', views.MovieDeleteView.as_view(), name='delete_movie'),
    path('movies/<int:movie_id>/edit_review/i<int:pk>/', views.InitialReviewUpdateView.as_view(), name='initial_review_edit' ),
    path('movies/<int:movie_id>/edit_review/r<int:pk>/', views.RewatchReviewUpdateView.as_view(), {'initial': False }, name='rewatch_review_edit'),
    path('reviews/delete_review/i<int:pk>/', views.InitialReviewDeleteView.as_view(), name='delete_initial_review'),
    path('by/<reviewer>/', views.reviews_by_reviewer, name="by_review"),
    path('search/', views.search, name="search"),
]
