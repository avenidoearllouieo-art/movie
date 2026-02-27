from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Avg
from .models import Movie, Review, Rating, Comment
from .serializers import MovieSerializer, ReviewSerializer, RatingSerializer, CommentSerializer

class MovieViewSet(ModelViewSet):
    """
    ViewSet for Movie CRUD operations.
    
    Provides endpoints for creating, listing, retrieving, updating, and deleting movies.
    Supports versioning via URL path (e.g., /api/v1/movies/).
    
    Custom Actions:
        - average_rating: Returns the average user rating for a specific movie.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None, **kwargs):
        """
        Calculate and return the average rating from all user ratings for a movie.
        
        GET /api/v1/movies/{id}/average_rating/
        
        Returns:
            Response: {'average_rating': float} or 0 if no ratings exist.
        """
        movie = self.get_object()
        ratings = movie.user_ratings.all()
        avg = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        return Response({'average_rating': avg})


class ReviewViewSet(ModelViewSet):
    """
    ViewSet for Review CRUD operations.
    
    Provides endpoints for managing movie reviews. Supports filtering by movie_id.
    
    Query Parameters:
        -(movie_id): Filter reviews for a specific movie (e.g., ?movie_id=1)
    
    Custom Actions:
        - mark_helpful: Increment the helpful count for a review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        """Filter reviews by movie_id if provided in query parameters."""
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            return Review.objects.filter(movie_id=movie_id)
        return Review.objects.all()
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None, **kwargs):
        """
        Mark a review as helpful by incrementing its helpful_count.
        
        POST /api/v1/reviews/{id}/mark_helpful/
        
        Returns:
            Response: {'helpful_count': int} updated count.
        """
        review = self.get_object()
        review.helpful_count += 1
        review.save()
        return Response({'helpful_count': review.helpful_count})


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            return Rating.objects.filter(movie_id=movie_id)
        return Rating.objects.all()


class CommentViewSet(ModelViewSet):
    """
    ViewSet for Comment CRUD operations.
    
    Manages comments on movies and reviews. Supports filtering by movie_id or review_id.
    
    Query Parameters:
        - movie_id: Filter comments for a specific movie (e.g., ?movie_id=1)
        - review_id: Filter comments for a specific review (e.g., ?review_id=1)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        """Filter comments by movie_id or review_id if provided in query parameters."""
        movie_id = self.request.query_params.get('movie_id')
        review_id = self.request.query_params.get('review_id')
        if movie_id:
            return Comment.objects.filter(movie_id=movie_id)
        if review_id:
            return Comment.objects.filter(review_id=review_id)
        return Comment.objects.all()


def homepage(request):
    movies = Movie.objects.all()
    total_movies = movies.count()
    recent_movies = movies.order_by('-release_year')[:5]
    
    # Add review counts and average ratings for each movie
    for movie in movies:
        movie.review_count = movie.reviews.count()
        ratings = movie.user_ratings.all()
        movie.average_user_rating = sum(r.rating for r in ratings) / ratings.count() if ratings.exists() else 0
    
    context = {
        'total_movies': total_movies,
        'recent_movies': recent_movies,
        'movies': movies,
    }
    return render(request, 'movies/homepage.html', context)