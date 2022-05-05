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

# viet 1 cai signal cho category
# if create thi set user
# if update thi check user is the right one

# @receiver(pre_save, sender=Category)
# def category_pre_save_receiver(sender, instance,raw,using,update_fields,*args, **kwargs):
#     """
#     before saved in the database
#     """
#     # print(instance.user)
#     print(using)
#     print(sender, instance,raw,using,update_fields, args, kwargs)
#     print(kwargs['signal'])
#     # if created:
#     #     print("Created")
#     # else:
#     #     print("Updated")
