from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods
User = get_user_model()
# Create your models here.
class ShoppingCart(models.Model):
    '''
    购物车
    '''
    user = models.ForeignKey(User, verbose_name=u'用户')
    goods = models.ForeignKey(Goods, verbose_name=u'商品')
    goods_num = models.IntegerFields(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.goods_num)

class OrderInfo(models.Model):
    pass