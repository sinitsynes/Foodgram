import base64
import uuid
import imghdr

from django.core.files.images import ImageFile
from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredients, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class Base64ToImageField(serializers.ImageField):
    def to_internal_value(self, data):
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            self.fail('Неподходящий файл для картинки')

        file_name = uuid.uuid4()[:8]
        file_extension = self.get_file_extension(file_name, decoded_file)
        complete_file_name = f'{file_name}.{file_extension}'
        data = ImageFile(decoded_file, name=complete_file_name)

        return super(Base64ToImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension

        return extension


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


# сериализатор чтения рецепта
class RecipeRetrieveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'tags',
            'author',
            'ingredients',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        queryset = RecipeIngredients.objects.filter(recipe=obj)
        return RecipeIngredientReadSerializer(queryset, many=True).data


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    amount = serializers.IntegerField()
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


# сериализатор создания рецепта
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

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeRetrieveSerializer(
            instance, context=context
        ).data
