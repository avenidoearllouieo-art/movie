from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class MovieAPITest(APITestCase):

    def test_create_movie(self):
        url = reverse('movie-list', kwargs={'version': 'v1'})
        data = {
            "title": "Inception",
            "director": "Christopher Nolan",
            "release_year": 2010,
            "rating": 4.8
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)