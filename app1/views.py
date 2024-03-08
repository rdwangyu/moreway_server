from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db.models import Sum
import json
import requests
import hashlib
from datetime import timedelta, datetime
from .models import *
from .serializers import *


@api_view(('GET',))
def category_list(request):
    top_category = Category.objects.values(
        'id', 'class_0').distinct('class_0')
    serializer = CategorySerializer(top_category, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def category_detail(request, name):
    sub_category = Category.objects.filter(class_0=name).values(
        'id', 'class_0', 'class_1', 'img').distinct('class_1')
    serializer = CategorySerializer(sub_category, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def banner_list(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(banner, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def banner_detail(request, id):
    try:
        banner = Banner.objects.get(pk=id)
        serializer = BannerSerializer(banner)
        return Response(data=serializer.data)
    except Banner.DoesNotExist:
        return Response(data={'errmsg': '无数据'})


@api_view(('GET',))
def goods_list(request):
    class_0 = request.GET.get('class_0')
    class_1 = request.GET.get('class_1')
    label = request.GET.get('label')
    keywords = request.GET.get('keywords')
    goods_id_list = request.GET.get('goods_id_list')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))

    goods = Goods.objects.filter(on_sale=True).order_by('-created_time')
    if class_1 and class_0:
        goods = goods.filter(category__class_0=class_0,
                             category__class_1=class_1)
    elif goods_id_list:
        goods_id_list = json.loads(goods_id_list)
        goods = goods.filter(id__in=goods_id_list)
    elif keywords:
        goods = goods.filter(name__contains=keywords)
    elif label:
        goods = goods.filter(label=label)
    goods = goods[(page - 1) * page_size: page * page_size]
    serializer = GoodsSerializer(goods, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def goods_detail(request, id):
    try:
        goods = Goods.objects.get(pk=id)
        serializer = GoodsSerializer(goods)
        return Response(data=serializer.data)
    except Goods.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
def search_list(request):
    search = Search.objects.order_by('click_times')
    serializer = SearchSerializer(search, many=True)
    return Response(data=serializer.data)


@api_view(('POST',))
def login(request):
    wxcode = request.POST.get('wxcode', '')
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type={}".format(
        'wx2576c4210717a45b',
        '0b673ab2dd780b5f5f64b2f04e311229',
        wxcode,
        'authorization_code')
    resp = requests.get(url)
    resp = resp.json()
    if 'errcode' in resp:
        ctx = {'errmsg': resp['errmsg'], 'errcode': resp['errcode']}
        return Response(data=ctx, status=status.HTTP_400_BAD_REQUEST)

    openid = resp['openid']
    session = hashlib.md5(
        (resp['session_key'] + openid + wxcode).encode('utf-8')).hexdigest()
    user, created = User.objects.update_or_create(
        wx_openid=openid,
        defaults={
            "wx_openid": openid,
            "login_session": session,
            "login_expired": timezone.now() + timedelta(days=30)
        })
    serializer = UserSerializer(user)
    return Response(data=serializer.data)


def _check_session(session):
    try:
        user = User.objects.get(login_session=session,
                                login_expired__gte=timezone.now())
        return (user, '')
    except User.DoesNotExist:
        return (None, '登录超时')


@api_view(('POST',))
def bill_list(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    page = int(request.POST.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))

    ctx = []
    cart = Cart.objects.filter(
        user=user, bill__isnull=False).order_by('-created_time')
    cart = cart[(page - 1) * page_size: page * page_size]
    serializer = CartSerializer(cart, many=True)
    for item in serializer.data:
        bill_id = item['bill']['id']
        goods_name_list = "{}\t￥{}-------x{}".format(
            item['goods']['name'],
            item['price'],
            str(item['num']))

        for i in range(len(ctx)):
            if ctx[i]['bill']['id'] == bill_id:
                ctx[i]['goods_name_list'].append(goods_name_list)
                break
        else:
            ctx.append({
                'bill': item['bill'],
                'cover': {
                    'goods_name': item['goods']['name'],
                    'img': item['goods']['thumbnail'][0]
                },
                'goods_name_list': [goods_name_list]
            })
    return Response(data=ctx)


@api_view(('POST',))
def bill_detail(request, id):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart.objects.filter(bill_id=id)
    serializer = CartSerializer(cart, many=True)
    return Response(data=serializer.data)


@api_view(('POST',))
def cart_list(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    goods_id_list = request.POST.get('goods_id_list')
    goods_id = request.POST.get('goods_id')
    if goods_id:
        cart, created = Cart.objects.get_or_create(
            user=user, goods_id=goods_id, bill__isnull=True)
        if not created:
            cart.num += 1
            cart.save()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    elif goods_id_list:
        goods_id_list = json.loads(goods_id_list)
        cart = Cart.objects.filter(
            user=user, pk__in=goods_id_list, bill__isnull=True)
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data)
    else:
        cart = Cart.objects.filter(user=user, bill__isnull=True)
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data)
    
@api_view(('POST',))
def cart_info(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    cnt = 0
    if user:
        cart = Cart.objects.filter(user=user, bill__isnull=True).aggregate(Sum('num'))
        cnt = cart['num__sum'] if cart['num__sum'] else 0
    return Response(data={'cnt': cnt})


@api_view(('PUT', 'DELETE'))
def cart_detail(request, id):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PUT':
        num = request.POST.get('num')
        cart = Cart.objects.filter(pk=id).update(num=num)
        ctx = {'msg': '更新成功'}
        return Response(data=ctx)
    elif request.method == 'DELETE':
        cart = Cart.objects.filter(user=user, goods_id=id, bill__isnull=True)
        cart.delete()
        ctx = {'msg': '删除成功'}
        return Response(data=ctx)


@api_view(('POST',))
def pay(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    cart_list = request.POST.get('cart_list')
    cart_list = json.loads(cart_list)
    user_info = request.POST.get('user_info')
    user_info = json.loads(user_info)

    total = {
        'payable': 0,
        'num': 0,
        'discount': 0,
    }
    bill = Bill()
    bill.save()
    bill = Bill.objects.latest('id')
    for i in range(len(cart_list)):
        data = cart_list[i]
        cart = Cart.objects.get(pk=data['id'])
        cart.num = data['num']
        cart.price = data['goods']['retail_price']
        cart.discount = data['discount']
        cart.bill = bill
        cart.save()

        total['payable'] += float(cart.num) * \
            float(cart.price) - float(cart.discount)
        total['num'] += cart.num

    bill.payable = total['payable']
    bill.num = total['num']
    bill.discount = total['discount']
    bill.sn = bill.created_time.strftime(
        "%Y%m%d%H%M%S") + str(bill.id).zfill(4)
    bill.save()

    user.addr = user_info['addr']
    user.phone = user_info['phone']
    user.name = user_info['name']
    user.save()

    serializers = BillSerializer(bill)
    return Response(data=serializers.data)


@api_view(('PUT',))
def user_detail(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    user.nickname = request.POST.get('nickname', '')
    user.save()
    serializers = UserSerializer(user)
    return Response(data=serializers.data)
