# Generated by Django 4.0.6 on 2022-09-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0009_remove_composer_genre_composer_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composer',
            name='genre',
            field=models.ManyToManyField(related_name='genre_composers', to='composers.genre'),
        ),
    ]
