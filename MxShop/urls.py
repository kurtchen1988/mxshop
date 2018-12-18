"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
# from django.urls import path
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter



from goods.views import GoodsListViewSet

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet)

goods_list = GoodsListViewSet.as_view({
    'get':'list',
})

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
   #url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),

    # 商品列表
    #url(r'goods/$', goods_list, name='goods-list'),
    url(r'^', include(router.urls)),

    url(r'docs/', include_docs_urls(title='暮学生鲜'))
]
