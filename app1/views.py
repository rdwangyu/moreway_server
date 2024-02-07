from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, Banner, Inventory, HotSearch, Cart, User, Bill
from .serializers import *
import json
import requests
import hashlib


@api_view(('GET',))
def getTopCategory(request):
    queryset = Category.objects.values('id', 'class0').distinct('class0')
    serializer = CategorySerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getCategory(request):
    topCategory = request.GET['category']
    queryset = Category.objects.filter(class0=topCategory).values(
        'id', 'class1', 'img').distinct('class1')
    serializer = CategorySerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getBanner(request):
    queryset = Banner.objects.values('id', 'img', 'url', 'remark')
    serializer = BannerSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getGoodsList(request):
    keywords = request.GET.get('keywords')
    page = int(request.GET.get('page'))
    queryset = Inventory.objects.values('id', 'goodsname', 'img', 'saleprice')
    if keywords:
        queryset = queryset.filter(goodsname__contains=keywords)
    queryset = queryset[(page - 1) * 50: page * 50]
    serializer = InventorySerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getGoodsDetail(request):
    id = request.GET.get('id')
    res = {}
    try:
        queryset = Inventory.objects.get(pk=id)
        serializer = InventorySingleSerializer(queryset)
        res = serializer.data
    except Inventory.DoesNotExist:
        res = {}
    return Response({'status': 200, 'data': res})


@api_view(('GET',))
def getBanner(request):
    queryset = Banner.objects.values('id', 'img', 'url', 'remark')
    serializer = BannerSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getHotSearch(request):
    queryset = HotSearch.objects.order_by(
        'clicktimes').values('id', 'text')[:7]
    serializer = HotSearchSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('POST',))
def getLogin(request):
    wxCode = request.POST['wxCode']
    res = requests.get(
        f"https://api.weixin.qq.com/sns/jscode2session?appid=wx2576c4210717a45b&secret=0b673ab2dd780b5f5f64b2f04e311229&js_code={ wxCode }&grant_type=authorization_code")
    res = res.json()
    print(res)
    sessionKey = res['session_key']
    openId = res['openid']
    session = hashlib.md5(
        (sessionKey + openId + wxCode).encode('utf-8')).hexdigest()
    print(session)
    try:
        obj = User.objects.get(openid=openId)
        obj.session = session
        obj.save()
    except User.DoesNotExist:
        obj = User(openid=openId, session=session)
        obj.save()

    serializer = UserSerializer(obj)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


def checkUserSession(request):
    allow = False
    userSession = request.POST['userSession'] if 'userSession' in request.POST else request.GET['userSession']
    user = None
    try:
        user = User.objects.get(session=userSession)
        allow = True
    except User.DoesNotExist:
        allow = False
    return {allow, user}


@api_view(('GET',))
def getOrderList(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    userId = request.GET['userId']
    queryset = Cart.objects.filter(user_id=userId).order_by('bill_id')
    serializer = CartSerializer(queryset, many=True)
    data = {}
    for item in serializer.data:
        orderId = item['bill']['id']
        goods_summary = item['inventory']['goodsname'] + \
            '\t x' + str(item['num'])
        if orderId in data:
            data[orderId]['bill'] = item['bill']
            data[orderId]['goods_summary'].append(goods_summary)
        else:
            data = {orderId: {
                'bill': item['bill'],
                'cover': {
                    'goods_name': item['inventory']['goodsname'],
                    'img': item['inventory']['img']
                },
                'goods_summary': [goods_summary]
            }}
    return Response({'status': 200, 'data': data})


@api_view(('GET',))
def getOrderDetail(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    orderId = request.GET['orderId']
    queryset = Cart.objects.filter(bill_id=orderId)
    serializer = CartSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getCart(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    queryset = Cart.objects.filter(user=user)
    serializer = CartSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def getCartGoods(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    goodsIdList = json.loads(request.GET.get('goodsIdList'))
    queryset = Cart.objects.filter(
        user=user, inventory_id__in=goodsIdList)
    serializer = CartSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def addCart(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    goodsId = int(request.GET['goodsId'])
    goodsNum = int(request.GET['num'])
    inventory = Inventory.objects.get(pk=goodsId)
    bill = Bill.objects.get(pk=1)
    print(user, 222222)
    obj = Cart(user=user, inventory=inventory, num=goodsNum, bill=bill)
    obj.save()
    return Response({'status': 200, 'msg': '添加成功'})


@api_view(('GET',))
def delCart(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    goodsId = int(request.GET['goodsId'])
    obj = Cart.objects.filter(user=user, inventory_id=goodsId)
    obj.delete()
    return Response({'status': 200, 'msg': '删除成功'})


@api_view(('POST',))
def pay(request):
    allow, user = checkUserSession(request)
    if not allow:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'msg': '未登录'})
    data = json.loads(request.POST['data'])
    goodsList = data['goodsList']
    addr = data['addr']

    total = {
        'payable': 0,
        'num': 0,
        'discount': 0,
    }

    obj = Bill(status=0)
    obj.save()
    billId = Bill.objects.latest('id')
    for i in range(len(goodsList)):
        order = goodsList[i]
        print(order)
        queryset = Cart.objects.get(pk=order['id'])
        queryset.num = order['num']
        queryset.price = order['inventory']['saleprice']
        queryset.discount = order['discount']
        queryset.bill = billId
        queryset.save()

        total['payable'] += queryset.num * queryset.price - queryset.discount
        total['num'] += queryset.num

    obj.payable = total['payable']
    obj.num = total['num']
    obj.discount = total['discount']
    obj.save()

    serializers = BillSerializer(obj)
    return Response(data=serializers.data, status=status.HTTP_200_OK)
