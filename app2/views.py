from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from app1.models import *
from app1.serializers import *
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime
import pytz


@api_view(('GET',))
def category_list(request):
    category = Category.objects.order_by(
        'class_0', 'class_1', 'ext_0', 'ext_1', 'ext_2', 'ext_3', 'ext_4')
    serializer = CategorySerializer(
        category, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET', 'POST', 'PUT'))
def goods_detail(request, barcode):
    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES
            print('POST data...', data, files)
            category = Category.objects.get(pk=int(data['category_id']))
            name = data['name']
            num = int(data['num'])
            retail_price = data['retail_price']
            cost_price = data['cost_price']
            brand = data['brand']
            remark = data['remark']
            on_sale = data['on_sale']
            goods = Goods(barcode=barcode, name=name, num=num,
                          retail_price=retail_price, cost_price=cost_price,
                          category=category, brand=brand, remark=remark,
                          on_sale=on_sale)
            if 'thumb' in files:
                goods.thumb = files['thumb']
            if 'poster' in files:
                goods.poster = files['poster']
            goods.save()
            serializer = GoodsSerializer(goods, context={'request': request})
            return Response(data=serializer.data)
        except Category.DoesNotExist:
            return Response(data={'errmsg': '分类不存在'})

    elif request.method == 'PUT':
        try:
            data = request.POST
            files = request.FILES
            print('PUT data...', data, files)
            goods = Goods.objects.get(barcode=barcode)
            category = Category.objects.get(pk=int(data['category_id']))
            goods.name = data['name']
            goods.num = data['num']
            goods.retail_price = data['retail_price']
            goods.cost_price = data['cost_price']
            goods.category = category
            goods.brand = data['brand']
            goods.remark = data['remark']
            goods.on_sale = data['on_sale']
            if 'thumb' in files:
                goods.thumb = files['thumb']
            if 'poster' in files:
                goods.poster = files['poster']
            goods.save()
            serializer = GoodsSerializer(goods, context={'request': request})
            return Response(data=serializer.data)
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '商品不存在, 数据异常' + barcode})
        except Category.DoesNotExist:
            return Response(data={'errmsg': '分类不存在'})

    elif request.method == 'GET':
        try:
            goods = Goods.objects.get(barcode=barcode)
            serializer = GoodsSerializer(goods, context={'request': request})
            return Response(data=serializer.data)
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '商品不存在'})


@api_view(('POST',))
def settle(request):
    if request.method == 'POST':
        cart_list = json.loads(request.body)
        total = {
            'payable': 0,
            'num': 0,
            'discount': 0,
        }
        Bill().save()
        bill = Bill.objects.latest('id')
        try:
            user = User.objects.get(wx_openid='oQIt866FNnOo7E-oSiSGG9D4MH5U')
            for i in range(len(cart_list)):
                id = cart_list[i]['id']
                price = cart_list[i]['retail_price']
                num = cart_list[i]['num']

                goods = Goods.objects.get(pk=id)
                goods.num -= num
                goods.save()

                cart = Cart(user=user, goods=goods,
                            num=num, price=price, bill=bill)
                cart.save()
                total['payable'] += float(cart.price) * \
                    float(cart.num) - float(cart.discount)
                total['num'] += num
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '数据异常, 商品不存在' + str(id)})
        except User.DoesNotExist:
            return Response(data={'errmsg': '数据异常, 管理员账号不存在'})
        except User.MultipleObjectsReturned:
            return Response(data={'errmsg': '数据异常, 管理员账号不唯一'})

        bill.payable = total['payable']
        bill.num = total['num']
        bill.discount = total['discount']
        bill.sn = bill.created_time.strftime(
            '%Y%m%d%H%M%S') + str(bill.id).zfill(4)
        bill.remark = '后台自动下单'
        bill.status = 3
        bill.save()

        serializer = BillSerializer(bill, context={'request': request})
        return Response(data=serializer.data)


@api_view(('GET',))
def bill_list(request):
    page_size = request.GET.get('page_size', 50)
    bill = Bill.objects.order_by('-created_time')
    bill = bill[0:page_size]
    serializer = BillSerializer(bill, many=True, context={'request': request})
    return Response(data=serializer.data)

@api_view()
def bill_is_online(request):
    bill = Bill.objects.filter(~Q(status=3))
    serializer = BillSerializer(bill, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET', 'PUT'))
def bill_detail(request, id):
    try:
        bill = Bill.objects.get(pk=id)
        if request.method == 'PUT':
            bill.status = request.POST['status']
            bill.save()
        cart = Cart.objects.filter(bill=bill)
        if not cart:
            return Response(data={'errmsg': '数据异常, 账单商品数据缺失' + str(id)})
        serializer = CartSerializer(
            cart, many=True, context={'request': request})
        return Response(data=serializer.data)
    except Bill.DoesNotExist:
        return Response(data={'errmsg': '数据异常, 账单不存在' + str(id)})


@api_view(('GET',))
def bill_stat(request):
    bill = Bill.objects.all()

    today = timezone.localtime().replace(hour=0, minute=0, second=0)
    this_week = today - timedelta(days=today.weekday())
    last_week = this_week - timedelta(weeks=1)
    this_month = today - timedelta(today.day) + timedelta(days=1)
    this_quarter = datetime(
        today.year, ((today.month - 1) // 3 + 1) * 3 - 2, 1, 0, 0, 0, tzinfo=pytz.UTC)

    total_today = bill.filter(
        created_time__gte=today).aggregate(Sum('payable'))
    total_this_week = bill.filter(
        created_time__gte=this_week).aggregate(Sum('payable'))
    total_last_week = bill.filter(
        created_time__gte=last_week, created_time__lt=this_week).aggregate(Sum('payable'))
    total_this_month = bill.filter(
        created_time__gte=this_month).aggregate(Sum('payable'))
    total_this_quarter = bill.filter(
        created_time__gte=this_quarter).aggregate(Sum('payable'))

    ctx = {
        'today': total_today['payable__sum'],
        'this_week': total_this_week['payable__sum'],
        'last_week': total_last_week['payable__sum'],
        'this_month': total_this_month['payable__sum'],
        'this_quarter': total_this_quarter['payable__sum'],
    }

    return Response(data=ctx)
