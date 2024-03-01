from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'
    
    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y-%m-%d %H:%M:%S")


class CartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    bill = BillSerializer()
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
