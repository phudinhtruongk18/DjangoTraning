from rest_framework import serializers

from product.my_validators import validate_name, unique_validator
from product.models import Product

# temp serializer photo
class TempPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField()

    class Meta:
        fields = ('photo')

class ShortProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk')
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    name = serializers.CharField(required=True, validators=[validate_name,unique_validator])
    views_count = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField()
    photos = TempPhotoSerializer(source='photo_set',many=True,write_only=True,required=False)
    
    class Meta:
        model = Product
        fields = ('owner','url','date_added', 'name', 'views_count', 'thumb','categories','photos')

    def get_owner(self, obj):
        if obj.owner:
            return obj.owner.username
        return None

    def get_views_count(self, obj):
        return obj.hit_count.hits

    def get_categories(self, obj):
        return obj.categories.values_list('name', flat=True)
        