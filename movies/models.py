from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=150)
    director = models.CharField(max_length=100)
    release_year = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return f"{self.title} ({self.release_year})"    