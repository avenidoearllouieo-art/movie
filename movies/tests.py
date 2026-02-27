from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Movie, Review, Rating, Comment

class MovieAPITest(APITestCase):
    """Test CRUD operations and validation for Movie endpoints."""

    def setUp(self):
        """Create sample movie for testing."""
        self.movie = Movie.objects.create(
            title="Inception",
            director="Christopher Nolan",
            release_year=2010,
            rating=4.8
        )

    def test_create_movie(self):
        """Test creating a movie via POST."""
        url = reverse('movie-list', kwargs={'version': 'v1'})
        data = {
            "title": "Interstellar",
            "director": "Christopher Nolan",
            "release_year": 2014,
            "rating": 4.7
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Interstellar")

    def test_list_movies(self):
        """Test listing all movies via GET."""
        url = reverse('movie-list', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_movie(self):
        """Test retrieving a single movie via GET."""
        url = reverse('movie-detail', kwargs={'version': 'v1', 'pk': self.movie.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Inception")

    def test_update_movie(self):
        """Test updating a movie via PUT."""
        url = reverse('movie-detail', kwargs={'version': 'v1', 'pk': self.movie.id})
        data = {
            "title": "Inception (Updated)",
            "director": "Christopher Nolan",
            "release_year": 2010,
            "rating": 4.9
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4.9)

    def test_delete_movie(self):
        """Test deleting a movie via DELETE."""
        url = reverse('movie-detail', kwargs={'version': 'v1', 'pk': self.movie.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())

    def test_invalid_rating_create(self):
        """Test that invalid rating (>5) is rejected on create."""
        url = reverse('movie-list', kwargs={'version': 'v1'})
        data = {
            "title": "Bad Movie",
            "director": "Unknown",
            "release_year": 2020,
            "rating": 10  # Invalid: should be 1-5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_future_release_year_rejected(self):
        """Test that future release year is rejected."""
        url = reverse('movie-list', kwargs={'version': 'v1'})
        data = {
            "title": "Future Movie",
            "director": "Unknown",
            "release_year": 2030,
            "rating": 4.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_together_constraint(self):
        """Test that unique constraint on (title, director, release_year) is enforced."""
        url = reverse('movie-list', kwargs={'version': 'v1'})
        data = {
            "title": "Inception",  # Same as setUp movie
            "director": "Christopher Nolan",
            "release_year": 2010,
            "rating": 3.5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_average_rating_action(self):
        """Test the average_rating custom action."""
        # Create some ratings
        Rating.objects.create(movie=self.movie, user_name="User1", rating=5)
        Rating.objects.create(movie=self.movie, user_name="User2", rating=4)
        
        # Construct URL manually since reverse() may not work with versioned action routes
        url = f'/api/v1/movies/{self.movie.id}/average_rating/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 4.5)


class ReviewAPITest(APITestCase):
    """Test CRUD operations for Review endpoints."""

    def setUp(self):
        """Create sample movie and review for testing."""
        self.movie = Movie.objects.create(
            title="Test Movie",
            director="Test Director",
            release_year=2020,
            rating=4.0
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user_name="TestUser",
            title="Great Movie",
            content="This is a great movie",
            rating=5
        )

    def test_create_review(self):
        """Test creating a review."""
        url = reverse('review-list', kwargs={'version': 'v1'})
        data = {
            "movie": self.movie.id,
            "user_name": "NewUser",
            "title": "Amazing",
            "content": "Loved it!",
            "rating": 4
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_reviews_filtered_by_movie(self):
        """Test filtering reviews by movie_id."""
        url = reverse('review-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_invalid_review_rating(self):
        """Test that review rating must be 1-5."""
        url = reverse('review-list', kwargs={'version': 'v1'})
        data = {
            "movie": self.movie.id,
            "user_name": "User",
            "title": "Bad",
            "content": "Bad",
            "rating": 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mark_helpful_action(self):
        """Test the mark_helpful custom action."""
        initial_count = self.review.helpful_count
        # Construct URL manually since reverse() may not work with versioned action routes
        url = f'/api/v1/reviews/{self.review.id}/mark_helpful/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['helpful_count'], initial_count + 1)


class RatingAPITest(APITestCase):
    """Test CRUD operations for Rating endpoints."""

    def setUp(self):
        """Create sample movie and rating for testing."""
        self.movie = Movie.objects.create(
            title="Test Movie",
            director="Test Director",
            release_year=2020,
            rating=4.0
        )

    def test_create_rating(self):
        """Test creating a rating."""
        url = reverse('rating-list', kwargs={'version': 'v1'})
        data = {
            "movie": self.movie.id,
            "user_name": "Rater1",
            "rating": 4
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_ratings_filtered_by_movie(self):
        """Test filtering ratings by movie_id."""
        Rating.objects.create(movie=self.movie, user_name="User1", rating=5)
        url = reverse('rating-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_invalid_rating_value(self):
        """Test that rating must be between 1 and 5."""
        url = reverse('rating-list', kwargs={'version': 'v1'})
        data = {
            "movie": self.movie.id,
            "user_name": "Rater",
            "rating": 0  # Invalid
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentAPITest(APITestCase):
    """Test CRUD operations for Comment endpoints."""

    def setUp(self):
        """Create sample movie, review, and comment for testing."""
        self.movie = Movie.objects.create(
            title="Test Movie",
            director="Test Director",
            release_year=2020,
            rating=4.0
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user_name="Reviewer",
            title="Review",
            content="Review content",
            rating=4
        )

    def test_create_comment(self):
        """Test creating a comment."""
        url = reverse('comment-list', kwargs={'version': 'v1'})
        data = {
            "movie": self.movie.id,
            "review": self.review.id,
            "user_name": "Commenter",
            "content": "Great review!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comments_filtered_by_movie(self):
        """Test filtering comments by movie_id."""
        Comment.objects.create(movie=self.movie, user_name="User1", content="Comment")
        url = reverse('comment-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_comments_filtered_by_review(self):
        """Test filtering comments by review_id."""
        Comment.objects.create(movie=self.movie, review=self.review, user_name="User1", content="Comment")
        url = reverse('comment-list', kwargs={'version': 'v1'})
        response = self.client.get(url, {'review_id': self.review.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)