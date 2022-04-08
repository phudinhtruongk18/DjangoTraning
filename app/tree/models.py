from django.db import models
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey

class MyNode(MPTTModel):
    """A tree model using MPTT."""
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


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

class Category(MPTTModel):
    """A simple node Category"""
    name = models.CharField(max_length=100)
    img = models.FileField()
    slug = models.SlugField(max_length=200,unique=True)
    products = models.ManyToManyField(Product, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
