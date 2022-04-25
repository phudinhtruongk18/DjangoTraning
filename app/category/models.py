from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin
from hitcount.models import HitCount
from sorl.thumbnail import get_thumbnail

from user.models import NomalUser


# class MyNode(MPTTModel):
class MyNode(models.Model):
    """My own tree model """
    # parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        abstract = True

    # node logic


class Category(MyNode, HitCountMixin):
    """A simple node Category"""
    user = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,unique = True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, blank=True, editable=False)
    image = models.ImageField(null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['date_added']

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('category:products_by_category', args=[self.slug])

    @property
    def thumbnail_url(self):
        # get first url photo or none
        if self.image:
            return get_thumbnail(self.image, '350x350', quality=90).url
        return None
