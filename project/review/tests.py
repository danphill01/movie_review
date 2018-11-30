import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Movie, Review


class ReviewModelTests(TestCase):
    
    def test_was_published_recently_with_future_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_review = Review(pub_date=time)
        self.assertIs(future_review.was_published_recently(), False)

    def test_was_published_recently_with_old_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_review = Review(pub_date=time)
        self.assertIs(future_review.was_published_recently(), False)

    def test_was_published_recently_with_recent_review(self):
        """
        was_published_recently() returns False for reviews whose pub_date is
        within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_review = Review(pub_date=time)
        self.assertIs(future_review.was_published_recently(), True)


def create_movie():
    """`
    creates a movie object
    """
    return Movie.objects.create(imdb_id='tt2262227', plot='Manolo, a young man who is torn between fulfilling the expectations of his family and following his heart, embarks on an adventure that spans three fantastic worlds where he must face his greatest fears.', runtime='1h 35min', rated='PG', title='The Book of Life', year=2014)


def create_review(movie, review_text, days):
    """`
    Create a review for a given movie with the given 'review_text' and published 
    the given number of 'days' offset to now (negative for reviews published 
    in the past, positive for reviews that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Review.objects.create(movie=movie, review_text=review_text, pub_date=time)


class ReviewIndexViewTests(TestCase):
    def test_no_reviews(self):
        """
        If no reviews exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('review:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No reviews are available.")
        self.assertQuerysetEqual(response.context['latest_review_list'], [])

    def test_past_review(self):
        """
        Reviews with a pub_date in the past are displayed on the index page.
        """
        movie = create_movie()
        create_review(movie=movie, review_text="Past review.", days=-30)
        response = self.client.get(reverse('review:index'))
        time = timezone.now() + datetime.timedelta(days=-30)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            ['<Review: The Book of Life - PG (2014): Past review. - {}>'.format(time.strftime("%I:%M%p %d%b%Y"))]
        )

    def test_future_review(self):
        """
        Reviews with a pub_date in the future aren't displayed on the index
        page.
        """
        movie = create_movie()
        create_review(movie=movie, review_text="Future review.", days=30)
        response = self.client.get(reverse('review:index'))
        self.assertContains(response, "No reviews are available")
        self.assertQuerysetEqual(response.context['latest_review_list'], [])

    def test_future_review_and_past_review(self):
        """
        Even if both past and future reviews exist, only past reviews are
        displayed.
        """
        movie = create_movie()
        create_review(movie=movie, review_text="Past review.", days=-30)
        create_review(movie=movie, review_text="Future review.", days=30)
        response = self.client.get(reverse('review:index'))

        time = timezone.now() + datetime.timedelta(days=-30)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            ['<Review: The Book of Life - PG (2014): Past review. - {}>'.format(time.strftime("%I:%M%p %d%b%Y"))]
        )

    def test_two_past_reviews(self):
        """
        The reviews index page may display multiple reviews.
        """
        movie = create_movie()
        create_review(movie=movie, review_text="Past review 1.", days=-30)
        create_review(movie=movie, review_text="Past review 2.", days=-5)
        response = self.client.get(reverse('review:index'))
        time1 = timezone.now() + datetime.timedelta(days=-30)
        time2 = timezone.now() + datetime.timedelta(days=-5)
        self.assertQuerysetEqual(
            response.context['latest_review_list'],
            [
              '<Review: The Book of Life - PG (2014): Past review 2. - {}>'.format(time2.strftime("%I:%M%p %d%b%Y")),
              '<Review: The Book of Life - PG (2014): Past review 1. - {}>'.format(time1.strftime("%I:%M%p %d%b%Y")),
            ]
        )


class ReviewDetailViewTests(TestCase):
    def test_future_review(self):
        """
        The detail view of a review with a pub_date in the future
        returns a 404 not found.
        """
        movie = create_movie()
        future_review = create_review(movie=movie, review_text="Future review.", days=5)
        url = reverse('review:review_detail', args=(future_review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_review(self):
        """
        The detail view of a review with a pub_date in the past
        displays the review's text
        """
        movie = create_movie()
        past_review = create_review(movie=movie, review_text="Past review.", days=-5)
        url = reverse('review:review_detail', args=(past_review.id,))
        response = self.client.get(url)
        self.assertContains(response, past_review.review_text)


