from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import json
import requests
import hashlib


@api_view(('GET',))
def category_list(request):
    top_category = Category.objects.values(
        'id', 'class_0').distinct('class_0')
    serializer = CategorySerializer(top_category, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def category_detail(request, name):
    sub_category = Category.objects.filter(class_0=name).values(
        'id', 'class_1', 'img').distinct('class_1')
    serializer = CategorySerializer(sub_category, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def banner_list(request):
    ad = Banner.objects.values('id', 'img', 'url', 'remark')
    serializer = BannerSerializer(ad, many=True)
    return Response(data=serializer.data)


@api_view(('GET',))
def goods_list(request):
    keywords = request.GET.get('keywords')
    print(111, keywords)
    some_id = request.GET.get('some_id')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))

    goods = Goods.objects.all()
    if some_id:
        some_id = json.loads(some_id)
        goods = goods.filter(id__in=some_id)
    if keywords:
        goods = goods.filter(name__contains=keywords)
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
    try:
        user = User.objects.get(wx_openid=openid)
        user.login_session = session
        user.save()
    except User.DoesNotExist:
        user = User(wx_openid=openid, login_session=session)
        user.save()

    serializer = UserSerializer(user)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


def _check_session(session):
    try:
        user = User.objects.get(login_session=session)
        return user
    except User.DoesNotExist:
        return None


@api_view(('POST',))
def bill_list(request):
    user = _check_session(request.POST.get('session', ''))
    if not user:
        ctx = {'errmsg': '未登录'}
        return Response(data=ctx, status=status.HTTP_401_UNAUTHORIZED)

    ctx = {}
    cart = Cart.objects.filter(user=user, bill__isnull=False).order_by('-bill')
    serializer = CartSerializer(cart, many=True)
    for item in serializer.data:
        bill_id = item['bill']['id']
        goods_name_list = item['goods']['name'] + \
            '\t x' + str(item['num'])
        if bill_id in ctx:
            ctx[bill_id]['bill'] = item['bill']
            ctx[bill_id]['goods_name_list'].append(goods_name_list)
        else:
            ctx = {
                bill_id: {
                    'bill': item['bill'],
                    'cover': {
                        'goods_name': item['goods']['name'],
                        'img': item['goods']['img']
                    },
                    'goods_name_list': [goods_name_list]
                }
            }
    return Response(data=ctx)


@api_view(('POST',))
def bill_detail(request, id):
    user = _check_session(request.POST.get('session', ''))
    if not user:
        ctx = {'errmsg': '未登录'}
        return Response(data=ctx, status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart.objects.filter(bill_id=id)
    serializer = CartSerializer(cart, many=True)
    return Response(data=serializer.data)


@api_view(('POST',))
def cart_list(request):
    user = _check_session(request.POST.get('session', ''))
    if not user:
        ctx = {'errmsg': '未登录'}
        return Response(data=ctx, status=status.HTTP_401_UNAUTHORIZED)

    cart = Cart.objects.filter(user=user)
    some_id = request.POST.get('some_id')
    if some_id:
        some_id = json.loads(some_id)
        cart = cart.filter(goods_id__in=some_id)
    serializer = CartSerializer(cart, many=True)
    return Response(data=serializer.data)


@api_view(('POST', 'DELETE'))
def cart_detail(request, id):
    user = _check_session(request.POST.get('session', ''))
    if not user:
        ctx = {'errmsg': '未登录'}
        return Response(data=ctx, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        num = int(request.POST.get('num', -1))
        goods = Goods.objects.get(pk=id)
        cart = Cart(user=user, goods=goods, num=num)
        cart.save()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        obj = Cart.objects.filter(user=user, goods_id=id)
        obj.delete()
        ctx = {'msg': '删除成功'}
        return Response(data=ctx)


@api_view(('POST',))
def pay(request):
    user = _check_session(request.POST.get('session', ''))
    if not user:
        ctx = {'errmsg': '未登录'}
        return Response(data=ctx, status=status.HTTP_401_UNAUTHORIZED)

    cart_list = request.POST.get('cart_list')
    cart_list = json.loads(cart_list)
    addr = request.POST.get('addr', '')

    total = {
        'payable': 0,
        'num': 0,
        'discount': 0,
    }

    bill = Bill(status=Bill.STATUS_ENUM[Bill.STATUS_WAIT_CONFIRM])
    bill.save()
    bill_id = Bill.objects.latest('id')

    print(cart_list, 44444)
    for i in range(len(cart_list)):
        order = cart_list[i]
        cart = Cart.objects.get(pk=order['id'])
        print(cart, 222)
        cart.num = order['num']
        cart.price = order['price']
        cart.discount = order['discount']
        cart.bill = bill_id
        cart.save()

        total['payable'] += cart.num * cart.price - cart.discount
        total['num'] += cart.num

    bill.payable = total['payable']
    bill.num = total['num']
    bill.discount = total['discount']
    bill.save()

    serializers = BillSerializer(bill)
    return Response(data=serializers.data)
