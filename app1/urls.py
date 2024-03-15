from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('banners', views.banner_list),
    path('banners/<int:id>', views.banner_detail),
    path('goods', views.goods_list),
    path('goods/<int:id>', views.goods_detail),
    path('searchs', views.search_list),
    path('categories', views.category_list),
    path('categories/<name>', views.category_detail),
    path('login', views.login),
    path('bills', views.bill_list),
    path('bills/<int:id>', views.bill_detail),
    path('carts', views.cart_list),
    path('carts/cnt', views.cart_info),
    path('carts/<int:id>', views.cart_detail),
    path('pay', views.pay),
    path('users', views.user_detail)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
