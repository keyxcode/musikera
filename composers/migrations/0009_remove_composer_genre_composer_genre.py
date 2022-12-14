# Generated by Django 4.0.6 on 2022-09-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0008_composer_genre_work_composer_alter_work_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composer',
            name='genre',
        ),
        migrations.AddField(
            model_name='composer',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, related_name='genre_composers', to='composers.genre'),
        ),
    ]
