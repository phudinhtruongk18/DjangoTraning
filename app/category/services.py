from .models import Category

from django.db import transaction


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
