# Generated by Django 2.2.16 on 2022-01-11 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=5, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('text', models.TextField(max_length=300, verbose_name='Описание рецепта')),
                ('cooking_time', models.DurationField(verbose_name='Время готовки')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(max_length=6, unique=True, verbose_name='HEX-код цвета')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('id',),
            },
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='recipes_tag_name_56fd94_idx'),
        ),
        migrations.AddField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipeingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]
