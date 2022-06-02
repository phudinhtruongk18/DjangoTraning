from typing import Iterable
from .models import Category
from user.models import NomalUser

def get_categories_by_owner(owner: NomalUser) -> Iterable[Category]:
    return Category.objects.filter(owner=owner)

