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
    retail_price = models.FloatField(default=0.0)
    cost_price = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(default='-')
    img = models.CharField(default='kong.png')
    remark = models.TextField(default='-')
    t = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    wx_openid = models.CharField(default='-')
    login_session = models.CharField(default='-')
    login_expired = models.DateTimeField(auto_now=True)
    nick_name = models.CharField(default='-')
    full_name = models.CharField(default='-')
    age = models.IntegerField(default=0)
    phone = models.CharField(default='-')
    addr = models.CharField(default='-')
    last_login = models.DateTimeField(auto_now=True)
    t = models.DateTimeField(auto_now_add=True)


class Search(models.Model):
    text = models.CharField(default='-')
    click_times = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    u = models.DateTimeField(auto_now=True)


class Bill(models.Model):
    PLATFORM_WX = 'WX'
    PLATFORM_CA = 'CA'
    PLATFORM_ZFB = 'ZFB'
    PAY_PLATFORM_ENUM = {
        PLATFORM_WX: 'WECHAT',
        PLATFORM_CA: 'CASH',
        PLATFORM_ZFB: 'ALIPAY'
    }
    STATUS_WAIT_CONFIRM = 'WAIT'
    STATUS_GET_READY = 'READY'
    STATUS_DILIVERY = 'DELIVERY'
    STATUS_FINISH = 'FINISH'
    STATUS_ENUM = {
        STATUS_WAIT_CONFIRM: 'Wait to confirm',
        STATUS_GET_READY: 'Get stock to ready',
        STATUS_DILIVERY: 'Delivery',
        STATUS_FINISH: 'Finish'
    }
    payable = models.FloatField(default=0.0)
    num = models.IntegerField(default=1)
    discount = models.FloatField(default=0.0)
    pay_platform = models.CharField(
        default=PLATFORM_WX, choices=PAY_PLATFORM_ENUM)
    status = models.CharField(
        default=STATUS_WAIT_CONFIRM, choices=STATUS_ENUM)
    t = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    bill = models.ForeignKey(Bill, null=True, on_delete=models.CASCADE)
    t = models.DateTimeField(auto_now_add=True)
