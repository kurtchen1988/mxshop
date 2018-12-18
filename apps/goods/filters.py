#from django_filters import rest_framework as filters
import django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    price_min = django_filters.NumberFilter(field_name='shop_price',lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price',lookup_expr='lte')
    #name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        fields = ['price_min','price_max']
        #fields = ['price_min','price_max','name']