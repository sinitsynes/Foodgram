import base64
import uuid
import imghdr

from django.core.files.images import ImageFile
from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


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


class RecipeSerializer(serializers.ModelSerializer):
    # image = Base64ToImageField()
    

    class Meta:
        fields = (
            'ingredients', 'tags', 'name', 'text', 'cooking_time'
        )
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
