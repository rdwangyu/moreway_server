from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.category_list),
    path('goods/<barcode>', views.goods_detail),
    path('settle', views.settle),
]