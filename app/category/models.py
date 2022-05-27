from django.db import IntegrityError, models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin
from hitcount.models import HitCount
from sorl.thumbnail import get_thumbnail

from user.models import NomalUser
# from .my_exception import CategoryValidationError
from django.core.exceptions import ValidationError

from django.dispatch import receiver
from django.db.models.signals import (
        post_save,
        pre_save,
)

from django.db.models import Q 


class CategoryQuerySet(models.QuerySet):
    def is_have_owner(self):
        return self.filter(owner__isnull=False)

    def search(self, query,owner=None):
        lookup = (Q(slug__icontains=query))
        qs = self.is_have_owner().filter(lookup)
        if owner is not None:
            qs2 = qs.filter(owner=owner)
            qs = (qs|qs2).distinct()
        return qs


class CategoryManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return CategoryQuerySet(self.model, using=self._db)
    
    def search(self, query,owner=None):
        lookup = (Q(name__icontains=query) | Q(date_added__icontains=query))
        qs = self.get_queryset().search(query,owner=owner)


class MyNode(models.Model):
    """My own abstract node model to implement tree structure"""
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        abstract = True


class Category(MyNode, HitCountMixin):
    """A node Category"""
    owner = models.ForeignKey(NomalUser, on_delete=models.SET_NULL,blank=False,null=True)
    name = models.CharField(max_length=200,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200,unique=True, editable=False)
    image = models.ImageField(null=True, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['date_added']

    # def clean(self):

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        if self.parent:
            if self.parent.slug == self.slug:
                raise ValidationError({'parent':'Parent slug and child slug must be different'})

        # validator
        self.full_clean()
        super(Category, self).save(*args, **kwargs)

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
