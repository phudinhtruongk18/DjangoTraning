# test nhu 1 chuyen gia 
# django tips from Sang Nguyen

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

import django

django.setup()


from category.models import Category 
from category.api.serializers import CustomCategorySerializer
from user.models import NomalUser

user = NomalUser.objects.first()
category =  Category.objects.create(name="test 2",owner=user)
# serializer = CustomCategorySerializer(categorys)

# print(serializer.data)


