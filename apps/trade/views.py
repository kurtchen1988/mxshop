import time
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
from utils.permissions import IsOwnerOrReadOnly

from .serializer import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

# Create your views here.
class ShoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物记录
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    #authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    #queryset = ShoppingCart.objects.all()
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)



class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    #authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer


    def perform_create(self, serializer):

        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_carts in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_carts.goods
            order_goods.goods_num = shop_carts.nums
            order_goods.order = order
            order_goods.save()

            shop_carts.delete()
        return order

from rest_framework.views import APIView
from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path, private_key_path
import datetime
from rest_framework.response import Response
#from django.shortcuts import redirect

class AlipayViewset(APIView):
    def get(self, request):
        '''
        处理支付宝的return_url返回
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,  # 私钥的位置
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            exsited_orders = OrderInfo.objects.filter(order_sn=order_sn)

            for exsited_order in exsited_orders:
                exsited_order.pay_status = trade_status
                exsited_orders.pay_no = trade_no
                exsited_orders.pay_time = datetime.now()
                exsited_orders.save()

            #from django.shortcuts import redirect
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            response = redirect('index')
            return response


    def post(self, request):
        '''
        处理支付宝的notify_url
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,  # 私钥的位置
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )


        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            exsited_orders = OrderInfo.objects.filter(order_sn = order_sn)

            for exsited_order in exsited_orders:
                exsited_order.pay_status = trade_status
                exsited_orders.pay_no = trade_no
                exsited_orders.pay_time = datetime.now()
                exsited_orders.save()

            return Response('success')