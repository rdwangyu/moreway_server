# Generated by Django 5.0.2 on 2024-03-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_goods_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
