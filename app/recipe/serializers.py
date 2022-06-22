"""
Serializers for recipe API.
"""
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for recipe."""
    
    class Meta:
        model = Recipe
        fields = [
            'id', 
            'title', 
            'time_minutes',
            'price',
            'link'
        ]
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for detail recipe view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']