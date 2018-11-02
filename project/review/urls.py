from django.urls import path

from . import views

app_name = 'review'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('m<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('m<int:movie_id>/comment/', views.comment, name='comment'),
]
