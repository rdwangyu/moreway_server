# Generated by Django 5.0.2 on 2024-03-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_goods_updated_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='thumb',
            field=models.ImageField(default='', upload_to='goods'),
        ),
    ]