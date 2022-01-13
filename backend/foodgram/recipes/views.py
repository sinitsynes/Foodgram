from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Ingredient, Recipe, Tag
from .serializers import (
    RecipeRetrieveSerializer,
    TagSerializer,
    RecipeDetailSerializer,
    IngredientSerializer
    )
from .permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeDetailSerializer
        if self.request.method == 'GET':
            return RecipeRetrieveSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
