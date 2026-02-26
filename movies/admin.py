from django.contrib import admin
from .models import Movie, Review, Rating, Comment

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'release_year', 'rating']
    search_fields = ['title', 'director']
    list_filter = ['release_year']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'user_name', 'rating', 'created_at', 'helpful_count']
    search_fields = ['title', 'movie__title', 'user_name']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user_name', 'rating', 'created_at']
    search_fields = ['movie__title', 'user_name']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'movie', 'created_at']
    search_fields = ['user_name', 'movie__title', 'content']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
