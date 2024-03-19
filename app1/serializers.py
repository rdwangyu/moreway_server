from rest_framework import serializers
from django.utils import timezone
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_img(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url) if obj.img else ''


class BannerSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_cover(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.cover.url) if obj.cover else ''

    def get_poster(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.poster.url) if obj.poster else ''


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    created_time = serializers.SerializerMethodField()
    thumb = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = '__all__'

    def get_created_time(self, obj):
        return timezone.localtime(obj.created_time).strftime('%Y-%m-%d %H:%M:%S')

    def get_thumb(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumb.url) if obj.thumb else ''

    def get_poster(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.poster.url) if obj.poster else ''


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
