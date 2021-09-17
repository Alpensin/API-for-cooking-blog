# Generated by Django 3.2.7 on 2021-09-17 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.RemoveIndex(
            model_name='ingredient',
            name='recipes_ing_title_0b970b_idx',
        ),
        migrations.RemoveIndex(
            model_name='tag',
            name='recipes_tag_title_21d184_idx',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='recipes_ing_name_164c6a_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='recipes_tag_name_56fd94_idx'),
        ),
    ]
