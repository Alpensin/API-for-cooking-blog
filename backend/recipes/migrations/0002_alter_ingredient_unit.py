# Generated by Django 3.2.7 on 2021-09-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(max_length=128, verbose_name='единица измерения'),
        ),
    ]
