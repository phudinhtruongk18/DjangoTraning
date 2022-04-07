from django.db import models
# Create your models here.

class MyNode(models.Model):
    """My simple Node to inherit"""
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    class Meta:
        abstract = True

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
    products = models.ManyToManyField(Product, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
