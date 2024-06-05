from django.test import TestCase
# app related imports
from .models import Actor, Movie, Review
from .serializers import MovieDetailSerializer, MovieListSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Tests for Movie related Serializers
class MovieSerializerTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name="act1", last_name="act1ln")
        self.movie_data = {
            'title': 'Matrix',
            'description': 'Matrix movie.',
            'actors': [self.actor]
        }
        self.movie = Movie.objects.create(title=self.movie_data['title'], description=self.movie_data['description'])
        self.movie.actors.add(self.actor)
        self.movie_list_serializer = MovieListSerializer(instance=self.movie)
        self.movie_detail_serializer = MovieDetailSerializer(instance=self.movie)

    def test_movie_list_serializer_contains_expected_fields(self):
        data = self.movie_list_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title']))

    def test_movie_detail_serializer_contains_expected_fields(self):
        data = self.movie_detail_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'description', 'actors', 'average_grade']))

    def test_movie_detail_serializer_actors_content(self):
        data = self.movie_detail_serializer.data
        self.assertEqual(data['actors'][0]['first_name'], self.actor.first_name)
        self.assertEqual(data['actors'][0]['last_name'], self.actor.last_name)

class MovieAPITestCase(APITestCase):
    def setUp(self):
        self.actor1 = Actor.objects.create(first_name="act1", last_name="ln1")
        self.actor2 = Actor.objects.create(first_name="act2", last_name="ln2")
        
        self.movie1 = Movie.objects.create(title="Matrix", description="Matrix movie.")
        self.movie2 = Movie.objects.create(title="movie2", description="a movie2.")
        
        self.movie1.actors.add(self.actor1, self.actor2)
        self.movie2.actors.add(self.actor1)
        
        Review.objects.create(grade=5, movie=self.movie1)
        Review.objects.create(grade=4, movie=self.movie1)
        Review.objects.create(grade=5, movie=self.movie2)

    def test_list_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], "Matrix")
        self.assertEqual(response.data['results'][1]['title'], "movie2")

    # UnitTests for the viewsets in /api endpoint  
    def test_retrieve_movie_details(self):
        url = reverse('movie-detail', args=[self.movie1.id])
        print(f"url : {url}")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Matrix")
        self.assertEqual(response.data['description'], "Matrix movie.")
        self.assertEqual(len(response.data['actors']), 2)
        self.assertEqual(response.data['actors'][0]['first_name'], "act1")
        self.assertEqual(response.data['actors'][0]['last_name'], "ln1")
        self.assertEqual(response.data['actors'][1]['first_name'], "act2")
        self.assertEqual(response.data['actors'][1]['last_name'], "ln2")
        self.assertEqual(response.data['average_grade'], 4.5)

        url = reverse('movie-detail', args=[self.movie2.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "movie2")
        self.assertEqual(response.data['description'], "a movie2.")
        self.assertEqual(len(response.data['actors']), 1)
        self.assertEqual(response.data['actors'][0]['first_name'], "act1")
        self.assertEqual(response.data['actors'][0]['last_name'], "ln1")
        self.assertEqual(response.data['average_grade'], 5.0)