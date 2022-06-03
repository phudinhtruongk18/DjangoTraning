from django.db.models.query import QuerySet

from django.db import transaction

from .models import Category

from common.services import model_update

# def create_category(* ,parent: Category,owner: NomalUser,name: str,image: InMemoryUploadedFile=None) -> Category:
@transaction.atomic
def create_category(* ,parent=None,owner=None,name =None,image=None) -> Category:
    # print('create_category')
    # print(parent)
    # print(owner)
    # print(name)
    # print(type(image))

    category = Category(parent=parent,owner=owner,name=name,image=image)
    category.full_clean()
    category.save()

    # do some another service or task here
    # may be celery

    return category

def category_update(*, category: Category, data) -> Category:
    fields = ['name', 'image']
    category, has_updated = model_update(instance=category, fields=fields, data=data)
    return category

def get_category_by_id(pk: int) -> Category:
    category = Category.objects.get(pk=pk)
    # get view count and product of that category
    category.views_count = category.()
    category.products = category.products_set.all()
    return category
    