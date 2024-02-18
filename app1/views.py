from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db.models import F
import json
import requests
import hashlib
from datetime import timedelta
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
    banner = Banner.objects.values('id', 'img', 'url', 'remark')
    serializer = BannerSerializer(banner, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def goods_list(request):
    class_0 = request.GET.get('class_0')
    class_1 = request.GET.get('class_1')
    label = request.GET.get('label')
    keywords = request.GET.get('keywords')
    some_id = request.GET.get('some_id')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))

    goods = Goods.objects.all().order_by('-t')
    if class_1 and class_0:
        goods = goods.filter(category__class_0=class_0, category__class_1=class_1)
    elif some_id:
        some_id = json.loads(some_id)
        goods = goods.filter(id__in=some_id)
    elif keywords:
        goods = goods.filter(name__contains=keywords)
    elif label:
        goods = goods.filter(label=label)
    goods = goods[(page - 1) * per_page: page * per_page]
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
    display_num = 7
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
    # resp = {'openid': '123', 'session_key': 'test123'} # for test
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
            "login_expired": timezone.now() + timedelta(days=3)})
    serializer = UserSerializer(user)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


def _check_session(session):
    try:
        user = User.objects.get(login_session=session,
                                login_expired__gte=timezone.now())
        user.login_expired += timedelta(days=3)
        user.save()
        return (user, '')
    except User.DoesNotExist:
        return (None, '登录超时')


@api_view(('POST',))
def bill_list(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    ctx = {}
    cart = Cart.objects.filter(user=user, bill__isnull=False).order_by('-bill')
    serializer = CartSerializer(cart, many=True)
    # print(serializer.data, 333)
    for item in serializer.data:
        bill_id = item['bill']['id']
        goods_name_list = "{}\t￥{}-------x{}".format(
            item['goods']['name'],
            item['price'],
            str(item['num']))
        if bill_id in ctx:
            ctx[bill_id]['goods_name_list'].append(goods_name_list)
        else:
            ctx[bill_id] = {
                'bill': item['bill'],
                'cover': {
                    'goods_name': item['goods']['name'],
                    'img': item['goods']['img']
                },
                'goods_name_list': [goods_name_list]
            }
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

    some_id = request.POST.get('some_id')
    goods_id = request.POST.get('goods_id')

    if goods_id:
        cart, created = Cart.objects.get_or_create(
            user=user, goods_id=goods_id, bill__isnull=True)
        if not created:
            cart.num += 1
            cart.save()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    elif some_id:
        some_id = json.loads(some_id)
        cart = Cart.objects.filter(
            user=user, pk__in=some_id, bill__isnull=True)
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data)
    else:
        cart = Cart.objects.filter(user=user, bill__isnull=True)
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data)


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

    total = {
        'payable': 0,
        'num': 0,
        'discount': 0,
    }
    userInfo = {
        'id': 0,
        'addr': '',
        'phone': '',
        'name': ''
    }

    bill = Bill()
    bill.save()
    bill_id = Bill.objects.latest('id')

    for i in range(len(cart_list)):
        order = cart_list[i]
        cart = Cart.objects.get(pk=order['id'])
        cart.num = order['num']
        cart.price = order['goods']['retail_price']
        cart.discount = order['discount']
        cart.bill = bill_id
        cart.save()

        total['payable'] += float(cart.num) * \
            float(cart.price) - float(cart.discount)
        total['num'] += cart.num

        userInfo['id'] = order['user']['id']
        userInfo['addr'] = order['user']['addr']
        userInfo['phone'] = order['user']['phone']
        userInfo['name'] = order['user']['name']

    bill.payable = total['payable']
    bill.num = total['num']
    bill.discount = total['discount']
    bill.save()

    user = User.objects.get(pk=userInfo['id'])
    user.addr = userInfo['addr']
    user.phone = userInfo['phone']
    user.name = userInfo['name']
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

