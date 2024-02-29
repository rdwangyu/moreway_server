from django.db import models


class Category(models.Model):
    class_0 = models.CharField(default='')
    class_1 = models.CharField(default='')
    ext_0 = models.CharField(default='')
    ext_1 = models.CharField(default='')
    ext_2 = models.CharField(default='')
    ext_3 = models.CharField(default='')
    ext_4 = models.CharField(default='')
    img = models.CharField(default='')


class Banner(models.Model):
    img = models.CharField(default='')
    url = models.CharField(default='')
    remark = models.TextField(default='')
    t = models.DateTimeField(auto_now_add=True)


class Goods(models.Model):
    name = models.CharField(default='')
    barcode = models.CharField(default='')
    num = models.IntegerField(default=0)
    retail_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    cost_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(default='')
    img = models.CharField(default='')
    label = models.IntegerField(default=0) # 11111101
    remark = models.TextField(default='')
    t = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    wx_openid = models.CharField(default='')
    login_session = models.CharField(default='')
    login_expired = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default='')
    nickname = models.CharField(default='')
    age = models.IntegerField(default=0)
    phone = models.CharField(default='')
    addr = models.CharField(default='')
    last_login = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Search(models.Model):
    text = models.CharField(default='')
    click_times = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)


class Bill(models.Model):
    sn = models.CharField(default='')
    payable = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    num = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    pay_platform = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    remark = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    bill = models.ForeignKey(Bill, default=0, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
