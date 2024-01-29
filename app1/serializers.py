from rest_framework import serializers
from .models import Category, Banner, Inventory, HotSearch, Cart, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'

class InventorySingleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'


class HotSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearch
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    inventory = InventorySingleSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
