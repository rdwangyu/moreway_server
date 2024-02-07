from django.urls import path

from . import views

urlpatterns = [
    path('gettopcategory/', views.getTopCategory, name='gettopcategory'),
    path('getcategory/', views.getCategory, name='getcategory'),
    path('getbanner/', views.getBanner, name='getbanner'),
    path('getgoodslist/', views.getGoodsList, name='getgoodslist'),
    path('getgoodsdetail/', views.getGoodsDetail, name='getgoodsdetail'),
    path('gethotsearch/', views.getHotSearch, name='gethotsearch'),
    path('getcart/', views.getCart, name='getcart'),
    path('addcart/', views.addCart, name='addcart'),
    path('delcart/', views.delCart, name='delcart'),
    path('getlogin/', views.getLogin, name='getlogin'),
    path('getorderdetail/', views.getOrderDetail, name='getorderdetail'),
    path('getorderlist/', views.getOrderList, name='getorderlist'),
    path('pay/', views.pay, name='pay'),
    path('getcartgoods/', views.getCartGoods, name='getcartgoods'),
]