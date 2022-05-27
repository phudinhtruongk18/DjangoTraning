from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.db.models import Count, F, Value

from product.my_validators import validate_name,validate_owner,unique_validator
from product.models import Product, Photo
from comment.api.serializers import CommentSerializer

from .short_serializers import CreateProductSerializer


class PhotoListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        photos = [Photo(**item) for item in validated_data]
        return Photo.objects.bulk_create(photos)


class PhotoSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),)
    image = serializers.ImageField(required=True)
    
    class Meta:
        model = Photo
        fields = ('product','image')
        # list_serializer_class = PhotoListSerializer


class ProductSerializer(CreateProductSerializer):
    "Same to CreateProductSerializer"
    name = serializers.CharField(required=False, validators=[unique_validator])

    slug = serializers.CharField(read_only=True)
    photos = PhotoSerializer(source="photo_set",many=True, read_only=True)
    comments = CommentSerializer(source="comment_set", read_only=True,many=True)
    thumb = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ('owner', 'date_added', 'slug', 'name', 'views_count','thumb','categories','photos', 'comments')
        
    def get_thumb(self, obj):
        thumb_url = obj.thumb
        return thumb_url


class ReportProductSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    hit_count = serializers.IntegerField(source='hit_count_generic__hits',read_only=True)

    class Meta:
        fields = ('name', 'hit_count')


class CommentProductSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    comments = CommentSerializer(source="comment_set", read_only=True,many=True)
    
    class Meta:
        fields = ('name', 'comments')

