# Generated by Django 4.1.5 on 2023-06-27 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_results_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='Slug',
            field=models.SlugField(unique=True),
        ),
    ]