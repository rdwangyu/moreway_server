from django.urls import path

from . import views

urlpatterns = [
    path('banners', views.banner_list),
    path('goods', views.goods_list),
    path('goods/<int:id>', views.goods_detail),
    path('searchs', views.search_list),
    path('categories', views.category_list),
    path('categories/<name>', views.category_detail),
    path('login', views.login),
    path('bills', views.bill_list),
    path('bills/<int:id>', views.bill_detail),
    path('carts', views.cart_list),
    path('carts/<int:id>', views.cart_detail),
    path('pay', views.pay),
    path('user', views.user_detail),

]