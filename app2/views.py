from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from app1.models import *
from app1.serializers import *


@api_view(('GET',))
def category_list(request):
    category = Category.objects.order_by(
        'class_0', 'class_1', 'ext_0', 'ext_1', 'ext_2', 'ext_3', 'ext_4')
    serializer = CategorySerializer(category, many=True)
    return Response(data=serializer.data)


@api_view(('GET', 'POST', 'PUT'))
def goods_detail(request, barcode):
    if request.method == 'POST':
        category = Category.objects.get(pk=request.POST.get('category_id'))
        num = request.POST.get('num')
        retail_price = request.POST.get('retail_price')
        cost_price = request.POST.get('cost_price')
        brand = request.POST.get('brand')
        remark = request.POST.get('remark')
        goods = Goods(barcode=barcode, num=num, retail_price=retail_price,
                      cost_price=cost_price, category=category,
                      brand=brand, remark=remark)
        goods.save()
        serializer = GoodsSerializer(goods)
        return Response(data=serializer.data)

    elif request.method == 'PUT':
        goods = Goods.objects.get(barcode=barcode)
        goods.name = request.POST.get('name')
        goods.num = request.POST.get('num')
        goods.retail_price = request.POST.get('retail_price')
        goods.cost_price = request.POST.get('cost_price')
        goods.category_id = request.POST.get('category_id')
        goods.brand = request.POST.get('brand')
        goods.remark = request.POST.get('remark')
        goods.save()
        serializer = GoodsSerializer(goods)
        return Response(data=serializer.data)

    elif request.method == 'GET':
        try:
            goods = Goods.objects.get(barcode=barcode)
            serializer = GoodsSerializer(goods)
            return Response(data=serializer.data)
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '无数据'})


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
            for i in range(len(cart_list)):
                id = cart_list[i]['id']
                price = cart_list[i]['retail_price']
                num = cart_list[i]['num']

                goods = Goods.objects.get(pk=id)
                goods.num -= num
                goods.save()

                cart = Cart(user_id=1, goods=goods,
                            num=num, price=price, bill=bill)
                cart.save()

                total['payable'] += float(cart.price) * \
                    float(cart.num) - float(cart.discount)
                total['num'] += num
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '数据异常, 商品不存在' + str(id)})

        bill.payable = total['payable']
        bill.num = total['num']
        bill.discount = total['discount']
        bill.sn = bill.t.strftime("%Y%m%d%H%M%S") + str(bill.id).zfill(4)
        bill.remark = '后台自动下单'
        bill.save()

        serializer = BillSerializer(bill)
        return Response(data=serializer.data)
