'''
Written by Samy <m.elsisi1995@gmail.com> on Wed 09.05.2023
Version 1.0
'''
from rest_framework import serializers
from . import models as m

class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer for list of recipe objects"""
    created_by = serializers.StringRelatedField()

    class Meta:
        model = m.Recipe
        fields = ['id', 'recipe_name', 'created_by', 'label']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe object"""

    class Meta:
        model = m.Recipe
        fields = '__all__'