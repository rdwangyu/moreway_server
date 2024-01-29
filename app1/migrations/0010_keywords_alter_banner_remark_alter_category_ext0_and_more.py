# Generated by Django 5.0.1 on 2024-01-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_rename_classid_inventory_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='-')),
                ('clicktimes', models.BigIntegerField(default=0)),
                ('t', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='banner',
            name='remark',
            field=models.TextField(default='-'),
        ),
        migrations.AlterField(
            model_name='category',
            name='ext0',
            field=models.CharField(default='-'),
        ),
        migrations.AlterField(
            model_name='category',
            name='ext1',
            field=models.CharField(default='-'),
        ),
        migrations.AlterField(
            model_name='category',
            name='ext2',
            field=models.CharField(default='-'),
        ),
        migrations.AlterField(
            model_name='category',
            name='ext3',
            field=models.CharField(default='-'),
        ),
        migrations.AlterField(
            model_name='category',
            name='ext4',
            field=models.CharField(default='-'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='remark',
            field=models.TextField(default='-'),
        ),
    ]
