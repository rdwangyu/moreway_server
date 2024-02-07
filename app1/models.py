from django.db import models
from datetime import datetime, timedelta


class Temp(models.Model):
    name = models.CharField(default='')


class Category(models.Model):
    class0 = models.CharField(default='未分类0')
    class1 = models.CharField(default='未分类1')
    img = models.CharField(default='-')
    ext0 = models.CharField(default='-')
    ext1 = models.CharField(default='-')
    ext2 = models.CharField(default='-')
    ext3 = models.CharField(default='-')
    ext4 = models.CharField(default='-')


class Banner(models.Model):
    img = models.CharField(default='-')
    url = models.CharField(default='/')
    remark = models.TextField(default='-')
    t = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    barcode = models.CharField(default='0')
    goodsname = models.CharField(default='-')
    num = models.IntegerField(default=0)
    saleprice = models.FloatField(default=0.0)
    inputprice = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(default='-')
    img = models.CharField(default='-')
    remark = models.TextField(default='-')
    t = models.DateTimeField(auto_now_add=True)


class HotSearch(models.Model):
    text = models.CharField(default='-')
    clicktimes = models.BigIntegerField(default=0)
    u = models.DateTimeField(auto_now=True)


class User(models.Model):
    openid = models.CharField(default='-')
    session = models.CharField(default='-')
    expired = models.DateTimeField(default=datetime.now() + timedelta(days=28))
    name = models.CharField(default='匿名')
    age = models.IntegerField(default='0')
    tel = models.CharField(default='01234567890')
    addr = models.CharField(default='-')
    lastlogin = models.DateTimeField(auto_now=True)
    t = models.DateTimeField(auto_now_add=True)


class Bill(models.Model):
    payable = models.FloatField(default=0.0)
    num = models.IntegerField(default=1)
    discount = models.FloatField(default=0.0)
    paytype = models.CharField(default='wx')
    status = models.IntegerField(default=0)
    t = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    t = models.DateTimeField(auto_now_add=True)
