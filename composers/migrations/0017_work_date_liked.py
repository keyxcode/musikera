# Generated by Django 4.0.6 on 2022-10-03 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0016_composer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='date_liked',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
