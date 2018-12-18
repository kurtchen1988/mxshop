from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from rest_framework import viewsets
from .models import Goods
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
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
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100



class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    #queryset = Goods.objects.all()
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter
    #filter_fields = ('name', 'shop_price')
'''
    def get_queryset(self):
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            queryset = self.queryset.filter(shop_price__gt=int(price_min))
        return queryset
'''