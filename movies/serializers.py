from rest_framework import serializers
from datetime import datetime
from .models import Movie, Review, Rating, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user_name', 'title', 'content', 'rating', 'created_at', 'updated_at', 'helpful_count', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at', 'helpful_count']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user_name', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    user_ratings = RatingSerializer(many=True, read_only=True)
    average_user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'release_year', 'rating', 'reviews', 'user_ratings', 'average_user_rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_release_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Release year cannot exceed current year.")
        return value

    def get_average_user_rating(self, obj):
        ratings = obj.user_ratings.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0