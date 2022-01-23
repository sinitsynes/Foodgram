import base64
import uuid
import imghdr
import datetime

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Favorite, Ingredient, Recipe,
    RecipeIngredients, ShoppingCart, Tag)
from users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class Base64ToImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            self.fail('Неподходящий файл для картинки')

        file_name = str(uuid.uuid4())[:8]
        file_extension = self.get_file_extension(file_name, decoded_file)
        complete_file_name = f'{file_name}.{file_extension}'
        data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ToImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension
        return extension


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


# сериализаторы чтения рецепта
class ShortRecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'tags',
            'author',
            'image',
            'ingredients',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        queryset = RecipeIngredients.objects.filter(recipe=obj)
        return RecipeIngredientReadSerializer(queryset, many=True).data

    def get_image(self, obj):
        return obj.image.url

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe=obj).exists()


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    amount = serializers.IntegerField()
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


# сериализаторы создания рецепта
class RecipeIngredientsWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ToImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientsWriteSerializer(many=True, required=True)

    class Meta:
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        model = Recipe
        read_only_fields = ('author',)

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients:
            RecipeIngredients.objects.get_or_create(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        RecipeIngredients.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredients.objects.get_or_create(
                recipe=instance,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )
        return instance

    def validate(self, data):
        ingredients = data['ingredients']
        list_ingredients = []
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля'
                )
            list_ingredients.append(ingredient['amount'])
        if not list_ingredients:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент'
            )
        if len(list_ingredients) != len(list(set(list_ingredients))):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )
        if data['cooking_time'] <= datetime.timedelta(0):
            raise serializers.ValidationError(
                'Время готовки должно быть больше нуля'
            )
        tags = data['tags']
        list_tags = []
        for tag in tags:
            list_tags.append(tag)
        if len(list_tags) != len(list(set(list_tags))):
            raise serializers.ValidationError(
                'Теги не должны повторяться'
            )
        return data

    def to_representation(self, instance):
        return RecipeRetrieveSerializer(instance).data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeListSerializer(instance.recipe).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShortRecipeListSerializer(instance.recipe).data
