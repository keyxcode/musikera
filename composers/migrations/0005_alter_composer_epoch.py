# Generated by Django 4.0.6 on 2022-09-16 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('composers', '0004_alter_composer_epoch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composer',
            name='epoch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='epoch_composers', to='composers.epoch'),
        ),
    ]
