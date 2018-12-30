import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Movie, InitialReview


def create_movie():
    """`
    creates a movie object
    """
    return Movie.objects.create(imdb_id='tt2262227', plot='Manolo, a young man who is torn between fulfilling the expectations of his family and following his heart, embarks on an adventure that spans three fantastic worlds where he must face his greatest fears.', runtime='1h 35min', rated='PG', title='The Book of Life', year=2014)


def create_review(movie, review_text, additional_text, user, days=0, hours=0, minutes=0, seconds=0, initial=True):
    """`
    Create a review for a given movie with the given 'review_text' and published 
    the given number of 'days' offset to now (negative for reviews published 
    in the past, positive for reviews that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if initial:
        return InitialReview.objects.create(movie=movie, review_text=review_text, watch_for=additional_text, pub_date=time, reviewer=user)
    return RewatchReview.objects.create(movie=movie, review_text=review_text, discovery=additional_text, pub_date=time, reviewer=user)




class ReviewModelTests(TestCase):
    
    def setUp(self):
        self.movie = create_movie()
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')


    def test_was_published_recently_with_future_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        in the future.
        """
        future_review = create_review(movie=self.movie, review_text="Future review.", additional_text="Something to watch for.", days=30, user=self.user)
        self.assertIs(future_review.was_published_recently(), False)

    def test_was_published_recently_with_old_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        older than 1 day.
        """
        past_review = create_review(movie=self.movie, review_text="Future review.", additional_text="Something to watch for.", days=-1, seconds=-1, user=self.user)
        self.assertIs(past_review.was_published_recently(), False)

    def test_was_published_recently_with_recent_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        within the last day.
        """
        past_review = create_review(movie=self.movie, review_text="Future review.", additional_text="Something to watch for.", user=self.user, hours=-23, minutes=-59, seconds=-59)
        self.assertIs(past_review.was_published_recently(), True)


class ReviewIndexViewTests(TestCase):
    def setUp(self):
        self.movie = create_movie()
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')


    def test_no_reviews(self):
        """
        If no reviews exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('review:review_list'))
        self.assertTemplateUsed(response, 'review/review_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No reviews are available.")
        self.assertQuerysetEqual(response.context['latest_review_list'], [])

    def test_past_review(self):
        """
        Reviews with a pub_date in the past are displayed on the index page.
        """
        create_review(movie=self.movie, review_text="Past review.", additional_text="Something to watch for.", days=-30, user=self.user)
        response = self.client.get(reverse('review:review_list'))
        time = timezone.now() + datetime.timedelta(days=-30)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            ['<InitialReview: The Book of Life - PG (2014): Past review. - {}>'.format(time.strftime("%I:%M%p %d%b%Y"))]
        )

    def test_future_review(self):
        """
        Reviews with a pub_date in the future aren't displayed on the index
        page.
        """
        create_review(movie=self.movie, review_text="Future review.", additional_text="Something to watch for.", days=30, user=self.user)
        response = self.client.get(reverse('review:review_list'))
        self.assertContains(response, "No reviews are available")
        self.assertQuerysetEqual(response.context['latest_review_list'], [])

    def test_future_review_and_past_review(self):
        """
        Even if both past and future reviews exist, only past reviews are
        displayed.
        """
        create_review(movie=self.movie, review_text="Past review.", additional_text="Something to watch for.", days=-30, user=self.user)
        create_review(movie=self.movie, review_text="Future review.", additional_text="Something to look forward to.", days=30, user=self.user)
        response = self.client.get(reverse('review:review_list'))

        time = timezone.now() + datetime.timedelta(days=-30)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            ['<InitialReview: The Book of Life - PG (2014): Past review. - {}>'.format(time.strftime("%I:%M%p %d%b%Y"))]
        )

    def test_two_past_reviews(self):
        """
        The reviews index page may display multiple reviews.
        """
        create_review(movie=self.movie, review_text="Past review 1.", additional_text="additional text 1", days=-30, user=self.user)
        create_review(movie=self.movie, review_text="Past review 2.", additional_text="additional text 2", days=-5, user=self.user)
        response = self.client.get(reverse('review:review_list'))
        time1 = timezone.now() + datetime.timedelta(days=-30)
        time2 = timezone.now() + datetime.timedelta(days=-5)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            [
              '<InitialReview: The Book of Life - PG (2014): Past review 2. - {}>'.format(time2.strftime("%I:%M%p %d%b%Y")),
              '<InitialReview: The Book of Life - PG (2014): Past review 1. - {}>'.format(time1.strftime("%I:%M%p %d%b%Y")),
            ]
        )


class ReviewDetailViewTests(TestCase):
    def setUp(self):
        self.movie = create_movie()
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')


    def test_future_review(self):
        """
        The detail view of a review with a pub_date in the future
        returns a 404 not found.
        """
        movie = create_movie()
        future_review = create_review(movie=movie, review_text="Future review.", additional_text="Some additional text.", days=5, user=self.user)
        url = reverse('review:initial_review_detail', args=(future_review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_review(self):
        """
        The detail view of a review with a pub_date in the past
        displays the review's text
        """
        movie = create_movie()
        past_review = create_review(movie=movie, review_text="Past review.", additional_text="Past additional text.", days=-5, user=self.user)
        url = reverse('review:initial_review_detail', args=(past_review.id,))
        response = self.client.get(url)
        self.assertContains(response, past_review.review_text)


class MovieDetailViewTests(TestCase):
    def test_movie_detail_view(self):
        movie = create_movie()
        url = reverse('review:movie_detail', args=(movie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movie, response.context['movie'])
