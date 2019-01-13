
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .models import Goods, GoodsCategory, GoodsImage, Banner, HotSearchWords
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, IndexCategorySerializer

# Create your views here.
'''
class GoodsListView(APIView):

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)

    def post(self, request, format=None):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
class GoodsListView(generics.ListAPIView):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
'''

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100



class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页，分页，搜索，过滤，排序
    '''
    #queryset = Goods.objects.all()
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    #authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')
    #filter_fields = ('name', 'shop_price')
    '''
    def get_queryset(self):
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            queryset = self.queryset.filter(shop_price__gt=int(price_min))
        return queryset
    '''
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取热搜词列表
    '''
    queryset = HotSearchWords
    serializer_class = HotWordsSerializer

class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品','酒水饮料'])
    serializer_class = IndexCategorySerializer