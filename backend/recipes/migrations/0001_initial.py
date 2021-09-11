# Generated by Django 3.2.7 on 2021-09-09 19:12

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='название ингредиента')),
                ('unit', models.CharField(max_length=128, unique=True, verbose_name='единица измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='IngredientForRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=1, max_digits=6, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество')),
            ],
            options={
                'db_table': 'foodgram_ingr_for_recipe',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='название рецепта')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to='recipe_images/', verbose_name='изображение')),
                ('description', models.TextField(verbose_name='текстовое описание')),
                ('cooking_time', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='время приготовления')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='название')),
                ('slug', models.SlugField(unique=True)),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18, unique=True)),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['title'], name='recipes_tag_title_21d184_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['slug'], name='recipes_tag_slug_3ea026_idx'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='in_favorites',
            field=models.ManyToManyField(blank=True, related_name='followed_recipes', to=settings.AUTH_USER_MODEL, verbose_name='в избранном'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientForRecipe', to='recipes.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='тэги'),
        ),
        migrations.AddField(
            model_name='ingredientforrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingredientsforrecipe', to='recipes.ingredient', verbose_name='ингредиент'),
        ),
        migrations.AddField(
            model_name='ingredientforrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientsforrecipe', to='recipes.recipe', verbose_name='рецепт'),
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['title'], name='recipes_ing_title_0b970b_idx'),
        ),
        migrations.AddField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(help_text='Выберите автора', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор для подписки'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписанный'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['title'], name='recipes_rec_title_9ebae8_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['slug'], name='recipes_rec_slug_412256_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['pub_date'], name='recipes_rec_pub_dat_caa7fa_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together={('author', 'title')},
        ),
        migrations.AddConstraint(
            model_name='ingredientforrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingr_recipe'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_following'),
        ),
    ]