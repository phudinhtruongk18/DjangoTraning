from rest_framework import serializers

from product.my_validators import validate_name, unique_validator
from product.models import Product


class ShortProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='pro_test_api_sing', lookup_field='pk')
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    name = serializers.CharField(required=True, validators=[validate_name,unique_validator])
    views_count = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = ('url','date_added', 'name', 'views_count', 'thumb','categories')

    def get_views_count(self, obj):
        return obj.hit_count.hits

    def get_categories(self, obj):
        return obj.categories.values_list('name', flat=True)