from django.db import IntegrityError, models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin
from hitcount.models import HitCount
from sorl.thumbnail import get_thumbnail

from user.models import NomalUser
from .my_exception import CategoryValidationError


class MyNode(models.Model):
    """My own abstract node model to implement tree structure"""
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        abstract = True


class Category(MyNode, HitCountMixin):
    """A node Category"""
    user = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,blank=False,null=True)
    name = models.CharField(max_length=200,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, editable=False)
    image = models.ImageField(null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        if not self.user:
            raise CategoryValidationError('User is not defined')
        if self.name:
            self.slug = slugify(self.name)
        if self.parent:
            if self.parent.slug == self.slug:
                raise CategoryValidationError('Parent slug and child slug must be different')

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
