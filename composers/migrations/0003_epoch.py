# Generated by Django 4.0.6 on 2022-09-14 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0002_composer_portrait'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epoch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epoch', models.CharField(max_length=255)),
            ],
        ),
    ]
