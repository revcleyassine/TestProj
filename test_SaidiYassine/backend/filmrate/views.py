from django.shortcuts import render

from rest_framework import viewsets
from django.core.cache import cache
from .models import Actor, Movie, Review
from .serializers import ActorSerializer, MovieListSerializer, MovieDetailSerializer, ReviewSerializer
from rest_framework.response import Response

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('movie')
    serializer_class = ReviewSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('title') 
    
    # I did use this mehtod to avoid creating multiple viewsets for every action 
    def get_serializer_class(self): 
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer
    
    # This method will handle the fethcing of movie details including it's related actors and the reviews average
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        cache_key = f'movie_{pk}_details'
        movie = cache.get(cache_key)
        if not movie:
            movie = Movie.objects.prefetch_related('actors', 'reviews').get(pk=pk)
            cache.set(cache_key, movie, 5)  # Cache pour 15 minutes
        serializer = self.get_serializer(movie) 
        return Response(serializer.data)

