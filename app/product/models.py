from django.db import models
# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from hitcount.models import HitCount
from hitcount.models import HitCountMixin

from user.models import NomalUser
from category.models import Category

from sorl.thumbnail import get_thumbnail


class Product(models.Model,HitCountMixin):
    """A product can have many categories"""
    user = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=30,unique = True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, blank=True, editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0)

    # class ProductObjects(models.Manager):
    #     def get_queryset(self):
    #         return super().get_queryset().filter(some fields = some querys)
            
    @property
    def price_display(self):
        return "$%s" % self.price

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product', args=[self.slug])

    @property
    def thumb(self):
        # get first url photo or ''
        try:
            photo = Photo.objects.filter(product=self)[:1].get()
            print("lof,",photo.thumbnail.url)
            return photo.thumbnail.url
            # return photo.image.url
        except Exception as e:
            print("Log photo:",e)
            return ''

class ProductInCategory(models.Model):
    """Iteam exist in Category"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'category',)

    def __str__(self):
        return str(self.category) + " - " +str(self.product)

    def __unicode__(self):
        return str(self.category) + " - " +str(self.product)

    @property
    def thumbnail_url(self):
        # get first url photo or none
        try:
            photo = Photo.objects.filter(product=self.product)[:1].get()
            return photo.thumbnail.url
            # return photo.image.url
        except Exception as e:
            print("Log photo:",e)
            return None


class Photo(models.Model):
    """Photos for products"""
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('product', 'id')

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(self.image, '350x350', quality=90)
        return None

    def __str__(self):
        return f"{self.product}"
