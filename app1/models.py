from django.db import models


class Category(models.Model):
    class_0 = models.CharField(default='未分类')
    class_1 = models.CharField(default='未分类')
    ext_0 = models.CharField(default='-')
    ext_1 = models.CharField(default='-')
    ext_2 = models.CharField(default='-')
    ext_3 = models.CharField(default='-')
    ext_4 = models.CharField(default='-')
    img = models.CharField(default='kong.png')


class Banner(models.Model):
    img = models.CharField(default='kong.png')
    url = models.CharField(default='-')
    remark = models.TextField(default='-')
    t = models.DateTimeField(auto_now_add=True)


class Goods(models.Model):
    name = models.CharField(default='-')
    barcode = models.CharField(default='0')
    num = models.IntegerField(default=0)
    retail_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.0)
    cost_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(default='-')
    img = models.CharField(default='kong.png')
    label = models.IntegerField(default=0) # 11111101
    remark = models.TextField(default='-')
    t = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    wx_openid = models.CharField(default='-')
    login_session = models.CharField(default='-')
    login_expired = models.DateTimeField(auto_now_add=True)
    name = models.CharField(null=True)
    nickname = models.CharField(null=True)
    age = models.IntegerField(default=0)
    phone = models.CharField(null=True)
    addr = models.CharField(null=True)
    last_login = models.DateTimeField(auto_now=True)
    t = models.DateTimeField(auto_now_add=True)


class Search(models.Model):
    text = models.CharField(default='-')
    click_times = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    u = models.DateTimeField(auto_now=True)


class Bill(models.Model):
    payable = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    num = models.IntegerField(default=1)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    pay_platform = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    t = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    bill = models.ForeignKey(Bill, null=True, on_delete=models.CASCADE)
    t = models.DateTimeField(auto_now_add=True)
