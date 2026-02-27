from rest_framework import serializers
from datetime import datetime
from .models import Movie, Review, Rating, Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    
    Fields:
        - id (read-only): Unique identifier
        - movie: Required foreign key reference to Movie
        - review: Optional foreign key reference to Review
        - user_name: Name of the commenter
        - content: Text content of the comment
        - created_at (read-only): Timestamp of creation
        - updated_at (read-only): Timestamp of last update
    """
    class Meta:
        model = Comment
        fields = ['id', 'movie', 'review', 'user_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model with nested comments.
    
    Fields:
        - id (read-only): Unique identifier
        - movie: Foreign key reference to Movie
        - user_name: Name of the reviewer
        - title: Review title
        - content: Full review text
        - rating: Rating 1-5 (validated)
        - created_at (read-only): Timestamp of creation
        - updated_at (read-only): Timestamp of last update
        - helpful_count (read-only): Number of times marked as helpful
        - comments (read-only, nested): Related comments on this review
        
    Validations:
        - rating must be between 1 and 5
    """
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user_name', 'title', 'content', 'rating', 'created_at', 'updated_at', 'helpful_count', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at', 'helpful_count']

    def validate_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for Rating model (user ratings for movies).
    
    Fields:
        - id (read-only): Unique identifier
        - movie: Foreign key reference to Movie
        - user_name: Name of the user who rated
        - rating: Rating 1-5 (validated)
        - created_at (read-only): Timestamp of creation
        
    Validations:
        - rating must be between 1 and 5
    """
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user_name', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model with nested reviews and ratings.
    
    Fields:
        - id (read-only): Unique identifier
        - title: Movie title
        - director: Director name
        - release_year: Year of release (validated: not in future)
        - rating: Movie rating 1-5 (validated)
        - reviews (read-only, nested): Related reviews for this movie
        - user_ratings (read-only, nested): Related user ratings for this movie
        - average_user_rating (read-only, calculated): Average of all user ratings
        
    Validations:
        - rating must be between 1 and 5
        - release_year cannot exceed current year
    """
    reviews = ReviewSerializer(many=True, read_only=True)
    user_ratings = RatingSerializer(many=True, read_only=True)
    average_user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'release_year', 'rating', 'reviews', 'user_ratings', 'average_user_rating']

    def validate_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_release_year(self, value):
        """Validate that release year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Release year cannot exceed current year.")
        return value

    def get_average_user_rating(self, obj):
        """
        Calculate the average rating from all user ratings for this movie.
        
        Args:
            obj: The Movie instance
            
        Returns:
            float: Average rating, or 0 if no ratings exist
        """
        ratings = obj.user_ratings.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0