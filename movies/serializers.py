from rest_framework import serializers
from datetime import datetime
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_release_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Release year cannot exceed current year.")
        return value