from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.db.models import Count, F, Value

from product.my_validators import validate_name,validate_owner,unique_validator
from product.models import Product, Photo
from comment.api.serializers import CommentSerializer
from category.api.serializers import ShortCategorySerializer

from .short_serializers import ShortProductSerializer


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_photo', lookup_field='pk',read_only=True)
    product = ShortProductSerializer(write_only=True)
    
    class Meta:
        model = Photo
        fields = ('url','image', 'product')


class ProductSerializer(ShortProductSerializer):
    "Same to ShortProductSerializer but change category method to serializer"
    slug = serializers.CharField(read_only=True)
    photos = PhotoSerializer(source="photo_set",many=True, read_only=True)
    comments = CommentSerializer(source="comment_set", read_only=True,many=True)
    thumb = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ('owner', 'date_added', 'slug', 'name', 'views_count','thumb','categories','photos', 'comments')
        
    def get_thumb(self, obj):
        request = self.context.get('request')
        thumb_url = obj.thumb
        return thumb_url


class ReportProductSerializer(ShortProductSerializer):

    class Meta:
        model = Product
        fields = ('name', 'views_count')
        
        
class CommentProductSerializer(ShortProductSerializer):
    comments = CommentSerializer(source="comment_set", read_only=True,many=True)
    
    class Meta:
        model = Product
        fields = ('name', 'comments')
