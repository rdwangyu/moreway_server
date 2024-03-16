# Generated by Django 5.0.2 on 2024-03-15 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_alter_goods_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='thumbnail',
        ),
        migrations.AlterField(
            model_name='banner',
            name='cover',
            field=models.ImageField(default='', upload_to='banner/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='poster',
            field=models.ImageField(default='', upload_to='banner/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(default='', upload_to='category/'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='poster',
            field=models.ImageField(default='', upload_to='goods/'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='thumb',
            field=models.ImageField(default='', upload_to='goods/'),
        ),
    ]