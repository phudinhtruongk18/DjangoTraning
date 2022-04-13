from django.db import models
# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey
from user.models import NomalUser
from django.template.defaultfilters import slugify

from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation

from sorl.thumbnail import get_thumbnail

class MyNode(MPTTModel):
    """A tree model using MPTT."""
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        abstract = True

    # node logic


class Product(models.Model):
    """A product can have many categories"""
    user = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=30,unique = True)
    img = models.FileField()
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, blank=True, editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Catalog(MyNode):
    """A simple node Category"""
    user = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,unique = True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, blank=True, editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Catalog, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ProductInCatalog(models.Model):
    """Iteam exist in catalog"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'catalog',)

    def __str__(self):
        return str(self.catalog) + " - " +str(self.product)

    def __unicode__(self):
        return str(self.catalog) + " - " +str(self.product)


class Photo(models.Model):
    """Photos for products"""
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(self.image, '50x50', quality=90)
        return None

    def __str__(self):
        return self.description


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(NomalUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
