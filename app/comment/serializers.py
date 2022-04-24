from rest_framework import serializers
from .models import Comment
from django.conf import settings
from django.db.models import Count, F, Value
from rest_framework.response import Response


# class CatalogSerializer(serializers.ModelSerializer):
#     views_count = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Catalog
#         fields = ('user', 'name', 'date_added', 'slug', 'image', 'views_count')

#     def get_views_count(self, obj) -> int:
#         # if not isinstance(obj, Catalog):
#         #     return None
#         return obj.hit_count.hits
