from django.db import models
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey


class MyNode(MPTTModel):
    """A tree model using MPTT."""
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    class Meta:
        abstract = True

    # node logic


class Product(models.Model):
    """A product can have many categories
    and a category can have many products
    that's why we use ManyToManyField
    """
    name = models.CharField(max_length=30)
    img = models.FileField()
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(MyNode):
    """A simple node Category"""
    name = models.CharField(max_length=100)
    img = models.FileField()
    slug = models.SlugField(max_length=200,unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class CategoryItem(MyNode):
    """Iteam exist in category"""
    # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.product
# Account
