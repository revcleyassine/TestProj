"""
to properly use async Views many parts of the app should support async mode , [ORM, midleware, db backend..]
so i did try to make hypotical changes in the following files :
    - views.py <this file>
    - settings ass commnented lines <at the end of the settings.py file> 
    - requirements file to add the needed dependencies for asgiref adynpg and databases for an aync-compatible database backens
"""

from rest_framework import viewsets
from django.core.cache import cache
from asgiref.sync import sync_to_async
from .models import Actor, Movie, Review
from .serializers import ActorSerializer, MovieListSerializer, MovieDetailSerializer, ReviewSerializer
from rest_framework.response import Response

class AsyncModelViewSet(viewsets.ModelViewSet):

    async def list(self, request, *args, **kwargs):
        queryset = await sync_to_async(list)(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    async def retrieve(self, request, *args, **kwargs):
        instance = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data)

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = await sync_to_async(self.get_object)()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data)

    async def destroy(self, request, *args, **kwargs):
        instance = await sync_to_async(self.get_object)()
        await sync_to_async(instance.delete)()
        return Response(status=204)

class ActorViewSet(AsyncModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class ReviewViewSet(AsyncModelViewSet):
    queryset = Review.objects.all().select_related('movie')
    serializer_class = ReviewSerializer

class MovieViewSet(AsyncModelViewSet):
    queryset = Movie.objects.all().order_by('title') 
    
    def get_serializer_class(self): 
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer
    
    async def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        cache_key = f'movie_{pk}_details'
        movie = await sync_to_async(cache.get)(cache_key)
        if not movie:
            movie = await sync_to_async(Movie.objects.prefetch_related('actors', 'reviews').get)(pk=pk)
            await sync_to_async(cache.set)(cache_key, movie, 60*15)  # Cache for 15 minutes
        serializer = self.get_serializer(movie)
        return Response(serializer.data)
