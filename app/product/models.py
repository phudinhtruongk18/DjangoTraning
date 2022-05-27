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


class Product(HitCountMixin,models.Model):
    """A product can have many categories"""
    owner = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,blank=False,null=True)
    name = models.CharField(max_length=200,unique = True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0)

    categories = models.ManyToManyField(Category,blank=False)

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
        ordering = ['date_added']

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product', args=[self.slug])

    @property
    def thumb(self):
        # get first url photo or ''
        try:
            photo = self.photo_set.first()
            return photo.thumbnail.url
            # return photo.image.url
        except Exception as e:
            # print("Log photo:",e)
            return ''


class Photo(models.Model):
    """Photos for products"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(self.image, '350x350', quality=90)
        return None

    def __str__(self):
        return f"{self.product}"
