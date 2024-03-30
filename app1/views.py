from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db.models.functions import Concat
from django.db.models import Sum, Q
import json
import requests
import hashlib
from datetime import timedelta
from .models import *
from .serializers import *


@api_view(('GET',))
def category_list(request):
    top_category = Category.objects.all().distinct(
        'class_0', 'priority').order_by('priority')
    serializer = CategorySerializer(
        top_category, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET',))
def category_detail(request, name):
    sub_category = Category.objects.filter(class_0=name).distinct('class_1')
    serializer = CategorySerializer(
        sub_category, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET',))
def banner_list(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(
        banner, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET',))
def banner_detail(request, id):
    try:
        banner = Banner.objects.get(pk=id)
        serializer = BannerSerializer(banner, context={'request': request})
        return Response(data=serializer.data)
    except Banner.DoesNotExist:
        return Response(data={'errmsg': '无数据'})


@api_view(('GET',))
def goods_list(request):
    print('GET params', request.GET)
    class_0 = request.GET.get('class_0')
    class_1 = request.GET.get('class_1')
    label = request.GET.get('label')
    keywords = request.GET.get('keywords')
    goods_id_list = request.GET.get('goods_id_list')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    include_off_sale = bool(int(request.GET.get('include_off_sale', 0)))

    goods = Goods.objects.all()
    if class_0:
        goods = goods.filter(category__class_0=class_0, on_sale=True)
        if class_1:
            goods = goods.filter(category__class_1=class_1)
        goods = goods.order_by('-updated_time')
    elif goods_id_list:
        goods_id_list = json.loads(goods_id_list)
        goods = goods.filter(on_sale=True, id__in=goods_id_list)
    elif keywords:
        goods = goods if include_off_sale else goods.filter(on_sale=True)
        goods = goods.annotate(category_full_name=Concat('category__class_0', 'category__class_1',
                                                         'category__ext_0', 'category__ext_1', 'category__ext_2', 'category__ext_3', 'category__ext_4'))
        goods = goods.filter(
            Q(name__icontains=keywords)
            | Q(category_full_name__icontains=keywords)
            | Q(barcode__icontains=keywords)).order_by('-updated_time')
    elif label:
        goods = goods.filter(
            on_sale=True, label=label).order_by('-updated_time')
    else:
        goods = goods.filter(on_sale=True).order_by('?')
    goods = goods[(page - 1) * page_size: page * page_size]
    serializer = GoodsSerializer(
        goods, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('GET', 'POST'))
def goods_detail(request, id):
    try:
        goods = Goods.objects.get(pk=id)
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            param = request.POST
            print(param)
            if 'thumb' in param:
                goods.thumb = request.FILES['file']
            if 'poster' in param:
                goods.poster = request.FILES['file']
            if 'name' in param:
                goods.name = param['name']
            if 'num' in param:
                goods.num = param['num']
            if 'remark' in param:
                goods.remark = param['remark']
            if 'cost_price' in param:
                goods.cost_price = param['cost_price']
            if 'retail_price' in param:
                goods.retail_price = param['retail_price']
            if 'brand' in param:
                goods.brand = param['brand']
            if 'category_id' in param:
                goods.category_id = param['category_id']
            if 'on_sale' in param:
                goods.on_sale = param['on_sale'] == 'true'
            goods.save()
        serializer = GoodsSerializer(goods, context={'request': request})
        return Response(data=serializer.data)
    except Goods.DoesNotExist:
        # todo 改成返回200+errmsg
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
def search_list(request):
    search = Search.objects.order_by('click_times')
    serializer = SearchSerializer(
        search, many=True, context={'request': request})
    return Response(data=serializer.data)


@api_view(('POST',))
def login(request):
    wxcode = request.POST.get('wxcode', '')
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type={}'.format(
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
            'wx_openid': openid,
            'login_session': session,
            'login_expired': timezone.now() + timedelta(days=30)
        })
    serializer = UserSerializer(user, context={'request': request})
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
    serializer = CartSerializer(cart, many=True, context={'request': request})
    for item in serializer.data:
        bill_id = item['bill']['id']
        goods_name_list = '{}\t￥{}-------x{}'.format(
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
                    'img': item['goods']['thumb']
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
    serializer = CartSerializer(cart, many=True, context={'request': request})
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
        serializer = CartSerializer(cart, context={'request': request})
        return Response(data=serializer.data)
    elif goods_id_list:
        goods_id_list = json.loads(goods_id_list)
        cart = Cart.objects.filter(
            user=user, pk__in=goods_id_list, bill__isnull=True)
        serializer = CartSerializer(
            cart, many=True, context={'request': request})
        return Response(data=serializer.data)
    else:
        cart = Cart.objects.filter(user=user, bill__isnull=True)
        serializer = CartSerializer(
            cart, many=True, context={'request': request})
        return Response(data=serializer.data)


@api_view(('POST',))
def cart_info(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    cnt = 0
    if user:
        cart = Cart.objects.filter(
            user=user, bill__isnull=True).aggregate(Sum('num'))
        cnt = cart['num__sum'] if cart['num__sum'] else 0
    return Response(data={'cnt': cnt})


@api_view(('PUT', 'DELETE'))
def cart_detail(request, id):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        cart = Cart.objects.get(pk=id)
        if request.method == 'PUT':
            num = request.POST.get('num')
            cart.num = num
            cart.save()
            ctx = {'msg': '更新成功'}
            return Response(data=ctx)
        elif request.method == 'DELETE':
            cart.delete()
            ctx = {'msg': '删除成功'}
            return Response(data=ctx)
    except Cart.DoesNotExist:
        return Response(data={'errmsg': '购物车不存在' + str(id)})


@api_view(('POST',))
def pay(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    cart_list = request.POST.get('cart_list')
    user_info = request.POST.get('user_info')
    bill_info = request.POST.get('bill_info')
    cart_list = json.loads(cart_list)
    user_info = json.loads(user_info)
    bill_info = json.loads(bill_info)

    total = {
        'payable': 0,
        'num': 0,
        'discount': 0,
    }
    bill = Bill()
    bill.save()
    bill = Bill.objects.latest('id')
    for i in range(len(cart_list)):
        try:
            data = cart_list[i]
            cart = Cart.objects.get(pk=data['id'])
            cart.num = data['num']
            cart.goods.num -= data['num']
            cart.price = data['goods']['retail_price']
            cart.discount = data['discount']
            cart.bill = bill
            cart.save()

            goods = Goods.objects.get(pk=data['goods']['id'])
            goods.num -= data['num']
            goods.save()
        except Cart.DoesNotExist:
            return Response(data={'errmsg': '购物车不存在' + str(data['id'])})
        except Goods.DoesNotExist:
            return Response(data={'errmsg': '商品不存在' + str(data['goods']['id'])})

        total['payable'] += float(cart.num) * \
            float(cart.price) - float(cart.discount)
        total['num'] += cart.num

    bill.payable = total['payable']
    bill.num = total['num']
    bill.discount = total['discount']
    bill.sn = bill.created_time.strftime(
        '%Y%m%d%H%M%S') + str(bill.id).zfill(4)
    bill.remark = bill_info['remark']
    bill.save()

    user.addr = user_info['addr']
    user.phone = user_info['phone']
    user.name = user_info['name']
    user.save()

    serializers = BillSerializer(bill, context={'request': request})
    return Response(data=serializers.data)


@api_view(('PUT',))
def user_detail(request):
    user, err_msg = _check_session(request.POST.get('session', ''))
    if not user:
        return Response(data={'errmsg': err_msg}, status=status.HTTP_401_UNAUTHORIZED)

    user.nickname = request.POST.get('nickname', '')
    user.save()
    serializers = UserSerializer(user, context={'request': request})
    return Response(data=serializers.data)
