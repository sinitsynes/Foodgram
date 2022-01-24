from django.contrib import admin

from .models import (Favorite, RecipeIngredient,
                     ShoppingCart, Tag, Recipe, Ingredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeIngredientsInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientsInLine,)

    def favorite_count(self, obj):
        return Favorite.objects.values('recipe_id').filter(
            recipe=obj).distinct().count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
