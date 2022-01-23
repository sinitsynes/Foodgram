from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import RecipeFilter, IngredientFilter
from .models import (
    Favorite, Ingredient,
    Recipe, RecipeIngredients,
    ShoppingCart, Tag
    )
from .serializers import (
    ShoppingCartSerializer,
    FavoriteSerializer,
    RecipeRetrieveSerializer,
    TagSerializer,
    RecipeCreateSerializer,
    IngredientSerializer
    )
# from .permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        if self.request.method == 'GET':
            return RecipeRetrieveSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        if user.is_anonymous:
            return queryset
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_favorited:
            queryset = queryset.filter(favorites__user=user)
        if is_in_shopping_cart:
            queryset = queryset.filter(cart__user=user)
        return queryset

    @action(detail=True, methods=['POST'],
            url_path='favorite')
    def add_to_fav(self, request, pk):
        user = request.user.id
        data = {'user': user, 'recipe': pk}
        context = {'request': request}
        serializer = FavoriteSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_to_fav.mapping.delete
    def delete_fav(self, request, pk):
        favorite = get_object_or_404(Favorite, recipe__id=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            url_path='shopping_cart')
    def add_to_cart(self, request, pk):
        user = request.user.id
        data = {'user': user, 'recipe': pk}
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_to_cart.mapping.delete
    def delete_from_cart(self, request, pk):
        favorite = get_object_or_404(ShoppingCart, recipe__id=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        recipes = RecipeIngredients.objects.filter(recipe__cart__user=user)
        ingredients = recipes.values(
            'ingredient__name',
            'ingredient__measurement_unit',
            ).annotate(total=Sum(
                'amount'))
        shopping_cart = []
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            total = ingredient['total']
            shopping_cart.append(
                f"{name}: {total} {measurement_unit}\n"
            )
        response = HttpResponse(shopping_cart, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shopping_cart.txt"'
        )
        return response


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None
