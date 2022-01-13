from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название тега',
        unique=True
    )
    color = models.CharField(
        max_length=6,
        verbose_name='HEX-код цвета',
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        indexes = [models.Index(fields=['name', ])]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=5,
        verbose_name='Единица измерения'
    )

    class Meta:
        indexes = [models.Index(fields=['name', ])]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Описание рецепта'
    )
    cooking_time = models.DurationField(
        verbose_name='Время готовки'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredients', related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )
