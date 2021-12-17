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
        indexes = [models.Index(fields=['name',])]

    def __str__(self):
        return self.name


class Ingredient(models.Mode):
    name = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=5,
        verbose_name='Единица измерения'
    )

    class Meta:
        indexes = [models.Index(fields=['name',])]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки'
    )
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)
    ingredients_amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id')

    def __str__(self):
        return self.name

