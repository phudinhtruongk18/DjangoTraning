# from django.test import TestCase

# # Create your tests here.

# from itertools import chain
# from typing import Iterable

# from .models import MyNode

# def get_decendants(node: MyNode) -> Iterable[MyNode]:
#     queryset = MyNode.objects.filter(parent=node)
#     results = chain(queryset)
#     for child in queryset:
#         results = chain(results, get_decendants(child))
#     return results

# list(get_decendants(MyNode.objects.get(pk=1)))

# create 2 example list
list1 = [1,2,3,4,5,6,7,8,9,10]
list2 = ["a","b","c","d","e","f","g","h","i","j"]
# check value
for x,y in zip(list1,list2):
    print(x,y)