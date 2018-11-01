from django.urls import path

from . import views

app_name = 'review'
urlpatterns = [
    path('', views.index, name="index"),
    path('m<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:review_id>/', views.review_detail, name='review_detail'),
    path('m<int:movie_id>/comment/', views.comment, name='comment'),
]
