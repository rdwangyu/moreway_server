# Generated by Django 5.0.1 on 2024-01-24 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
