from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, Banner, Inventory, HotSearch, Cart, User, Bill
from .serializers import (CategorySerializer, BannerSerializer, UserSerializer,
                          InventorySerializer, InventorySingleSerializer, HotSearchSerializer, CartSerializer)
import json


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
    goodsIdList = request.GET.get('goodsIdList')
    page = int(request.GET.get('page'))
    queryset = Inventory.objects.values('id', 'goodsname', 'img', 'saleprice')
    if goodsIdList:
        queryset = queryset.filter(pk__in=json.loads(goodsIdList))
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


@api_view(('GET',))
def getCart(request):
    queryset = Cart.objects.filter(user_id=1)
    serializer = CartSerializer(queryset, many=True)
    return Response({'status': 200, 'data': serializer.data})


@api_view(('GET',))
def addCart(request):
    userId = int(request.GET['userId'])
    goodsId = int(request.GET['goodsId'])
    goodsNum = int(request.GET['num'])
    user = User.objects.get(pk=userId)
    inventory = Inventory.objects.get(pk=goodsId)
    num = goodsNum
    bill = Bill.objects.get(pk=1)
    obj = Cart(user=user, inventory=inventory, num=num, bill=bill)
    obj.save()
    return Response({'status': 200, 'msg': '添加成功'})


@api_view(('GET',))
def delCart(request):
    userId = int(request.GET['userId'])
    goodsId = int(request.GET['goodsId'])
    obj = Cart.objects.filter(user_id=userId, inventory_id=goodsId)
    obj.delete()
    return Response({'status': 200, 'msg': '删除成功'})


@api_view(('POST',))
def getLogin(request):
    wxCode = request.POST['wxCode']
    try:
        obj = User.objects.get(wxid=wxCode)
    except User.DoesNotExist:
        obj = User(wxid=wxCode)
        obj.save()

    serializer = UserSerializer(obj)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
