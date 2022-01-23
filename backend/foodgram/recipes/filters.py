from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug')
    author = filters.NumberFilter(
        field_name='author__id'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(SearchFilter):
    search_param = 'name'
