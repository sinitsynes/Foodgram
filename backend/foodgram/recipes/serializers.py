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
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'text',
            'cooking_time'
        )


# сериализаторы для создания рецепта
class RecipeTagDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',)


class RecipeIngredientDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeDetailSerializer(serializers.ModelSerializer):
    # image = Base64ToImageField()
    tags = RecipeTagDetailSerializer(many=True)
    ingredients = RecipeIngredientDetailSerializer(many=True)

    class Meta:
        fields = (
            'author', 'ingredients', 'tags', 'name', 'text', 'cooking_time'
        )
        model = Recipe
        read_only_fields = ('author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag, value = Tag.objects.get(**tag)
            recipe.tag.objects.create(
                tag=current_tag, recipe=recipe
            )
        return recipe
