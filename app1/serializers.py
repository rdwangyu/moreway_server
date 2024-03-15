from rest_framework import serializers
from django.utils import timezone
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    thumbnail = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    thumb = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = '__all__'

    def get_thumbnail(self, obj):
        return obj.thumbnail.split(';')

    def get_poster(self, obj):
        return obj.poster.split(';')

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_thumb(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumb.url)
    def get_poster(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.poster.url)


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_last_login(self, obj):
        return timezone.localtime(obj.last_login).strftime('%Y-%m-%d %H:%M:%S')


class BillSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')


class CartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    bill = BillSerializer()
    user = UserSerializer()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')
