from django.test import TestCase

# Create your tests here.

from itertools import chain
from typing import Iterable

from .models import MyNode

def get_decendants(node: MyNode) -> Iterable[MyNode]:
    queryset = MyNode.objects.filter(parent=node)
    results = chain(queryset)
    for child in queryset:
        results = chain(results, get_decendants(child))
    return results

list(get_decendants(MyNode.objects.get(pk=1)))