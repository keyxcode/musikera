# Generated by Django 4.0.6 on 2022-10-03 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0017_work_date_liked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='date_liked',
            new_name='liked_date_time',
        ),
    ]
