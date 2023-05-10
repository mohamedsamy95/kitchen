'''
Written by Samy <m.elsisi1995@gmail.com> on Wed 09.05.2023
Version 1.0
'''
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from . import models as m
from . import serializers as s
from django.http import HttpRequest

from django.core.cache import cache

CACHE_TIME = 60 * 15 #Cache elements should be evacuated after 15 minutes


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = s.RecipeSerializer
    queryset = m.Recipe.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['recipe_name', 'created_by', 'label']

    def retrieve(self, request:HttpRequest, pk=None):
        #Check if entry exists in cache
        cache_key = 'recipe_{}'.format(str(pk))
        data = cache.get(cache_key)

        #If entry exists, return
        if data:
            print('CACHE HIT')
            return Response(data)
        
        #If not, store data in cache and return it
        print('CACHE MISS')
        queryset = m.Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = s.RecipeSerializer(recipe)
        cache.set(cache_key, serializer.data, CACHE_TIME)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = request.user.pk #Automatically set the field "created_by" to current user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        #Update cache
        cache_key = 'recipe_{}'.format(str(serializer.data['id']))
        cache.set(cache_key, serializer.data, CACHE_TIME)

        #Return response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        #Update cache
        cache_key = 'recipe_{}'.format(str(response.data['id']))
        cache.set(cache_key, response.data, CACHE_TIME)

        return response
    
    def destroy(self, request, pk):
        queryset = m.Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(recipe)

        #Invalidate cache
        cache_key = 'recipe_{}'.format(str(pk))
        cache.delete(cache_key)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = s.RecipeListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = s.RecipeListSerializer(queryset, many=True)
        return Response(serializer.data)

