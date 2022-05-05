from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.db.models import Count, F, Value

from category.my_validators import validate_name,validate_owner,unique_validator
from category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category:test_api_sing', lookup_field='pk')
    owner = serializers.SerializerMethodField('_owner',validators=[validate_owner])
    # parent = serializers.CharField(source='parent.name')
    parent = serializers.SerializerMethodField()
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)
    slug = serializers.CharField(read_only=True)
    
    name = serializers.CharField(required=True, validators=[validate_name,unique_validator])

    class Meta:
        model = Category
        # fields = ('current_user','user', 'parent','slug', 'name', 'date_added', 'image', 'views_count')
        fields = ('url','owner', 'parent','slug', 'name', 'date_added', 'image', 'views_count')

    def get_views_count(self, obj):
        # if not isinstance(obj, Catalog):
        #     return None
        return obj.hit_count.hits

    # def get_image_url(self, obj):
    #     return obj.image.url

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
        return None

    #    # Use this method for the custom field
    def _owner(self, obj):
        if obj.owner:
            return obj.owner.username
        return None
