# Generated by Django 5.0.2 on 2024-03-16 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(default='', upload_to='banner/')),
                ('poster', models.ImageField(default='', upload_to='banner/')),
                ('remark', models.TextField(default='')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(default='')),
                ('payable', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('num', models.IntegerField(default=0)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('pay_platform', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('remark', models.TextField(default='')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_0', models.CharField(default='')),
                ('class_1', models.CharField(default='')),
                ('ext_0', models.CharField(default='')),
                ('ext_1', models.CharField(default='')),
                ('ext_2', models.CharField(default='')),
                ('ext_3', models.CharField(default='')),
                ('ext_4', models.CharField(default='')),
                ('img', models.ImageField(default='', upload_to='category/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wx_openid', models.CharField(default='')),
                ('login_session', models.CharField(default='')),
                ('login_expired', models.DateTimeField(default='1970-01-01')),
                ('name', models.CharField(default='')),
                ('nickname', models.CharField(default='')),
                ('age', models.IntegerField(default=0)),
                ('phone', models.CharField(default='')),
                ('addr', models.CharField(default='')),
                ('role', models.IntegerField(default=1)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='')),
                ('barcode', models.CharField(default='')),
                ('num', models.IntegerField(default=0)),
                ('retail_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('label', models.IntegerField(default=0)),
                ('brand', models.CharField(default='')),
                ('remark', models.TextField(default='')),
                ('on_sale', models.BooleanField(default=False)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('thumb', models.ImageField(default='', upload_to='goods/')),
                ('poster', models.ImageField(default='', upload_to='goods/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app1.category')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='')),
                ('click_times', models.BigIntegerField(default=0)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.bill')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
    ]
