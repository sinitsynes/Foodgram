from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeRetrieveSerializer,
                          ShoppingCartSerializer, TagSerializer)


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
    permission_classes = (IsAuthorOrStaffOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeCreateSerializer
        if self.request.method == 'GET':
            return RecipeRetrieveSerializer

    def common_add_method(self, request, pk, serializer_class):
        """Общий метод для добавления в избранное и в корзину."""

        user = request.user.id
        data = {'user': user, 'recipe': pk}
        serializer = serializer_class(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def common_del_method(self, request, pk, model):
        """Общий метод для удаления из избранного и корзины."""

        obj = get_object_or_404(model, recipe__id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            url_path='favorite')
    def add_to_fav(self, request, pk):
        return self.common_add_method(request, pk, FavoriteSerializer)

    @add_to_fav.mapping.delete
    def delete_fav(self, request, pk):
        return self.common_del_method(request, pk, Favorite)

    @action(detail=True, methods=['POST'],
            url_path='shopping_cart')
    def add_to_cart(self, request, pk):
        return self.common_add_method(request, pk, ShoppingCartSerializer)

    @add_to_cart.mapping.delete
    def delete_from_cart(self, request, pk):
        return self.common_del_method(request, pk, ShoppingCart)

    @action(detail=False, methods=['GET'],
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        recipes = RecipeIngredient.objects.filter(recipe__cart__user=user)
        ingredients = recipes.values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(total=Sum('amount'))
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
