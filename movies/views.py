from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

def homepage(request):
    movies = Movie.objects.all()
    total_movies = movies.count()
    recent_movies = movies.order_by('-release_year')[:5]
    
    context = {
        'total_movies': total_movies,
        'recent_movies': recent_movies,
        'movies': movies,
    }
    return render(request, 'movies/homepage.html', context)