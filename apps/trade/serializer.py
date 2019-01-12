from rest_framework import serializers
import time
from goods.models import Goods

from .models import ShoppingCart, OrderInfo, OrderGoods

from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = '__all__'

class OrderGoodsSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'

class ShopCartSerializer(serializers.Serializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'min_value':'商品数量不能小于一',
                                        'required':'请选择购买数量',
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        exsited = ShoppingCart.objects.filter(user=user, goods=goods)

        if exsited:
            exsited = exsited[0]
            exsited.nums += nums
            exsited.save()
        else:
            exsited = ShoppingCart.objects.create(**validated_data)

        return exsited

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

class OrderDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)

    trade_no = serializers.CharField(read_only=True)

    order_sn = serializers.CharField(read_only=True)

    pay_time = serializers.DateTimeField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)


    def get_alipay_url(self, obj):

        alipay = AliPay(
            appid="",
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,  # 私钥的位置
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            #return_url="http://127.0.0.1:8000/alipay/return/"
            return_url=""
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url


    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime('%Y%m%d%H%M%S'), userid=self.context['request'].user.id, ranstr=random_ins.randint(10, 99))

        return order_sn

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return
        return OrderSerializer

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
