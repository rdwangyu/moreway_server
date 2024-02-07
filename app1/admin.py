from django.contrib import admin
from .models import Category, Banner, Inventory, HotSearch, Cart, Bill, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'class0', 'class1',
                    'ext0', 'ext1', 'ext2', 'ext3', 'ext4', 'img']
    list_filter = ['class0']
    list_per_page = 50


class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'img', 'url', 't']


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'barcode', 'goodsname', 'num',
                    'saleprice', 'inputprice', 'category', 'img', 'brand', 'remark', 't']


class HotSearchAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'clicktimes', 'u']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventory', 'num', 'price',
                    'discount', 'user', 'bill', 't']


class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'payable', 'num',
                    'discount', 'paytype', 'status', 't']


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'session', 'expired', 'name',
                    'age', 'tel', 'addr', 'lastlogin', 't']


admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(HotSearch, HotSearchAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(User, UserAdmin)
