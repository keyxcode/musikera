# Generated by Django 4.0.6 on 2022-09-19 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0010_alter_composer_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='composer',
            old_name='genre',
            new_name='genres',
        ),
    ]
