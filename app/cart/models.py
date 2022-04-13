from django.db import models


# Create your models here.
from tree.models import ProductInCatalog, Catalog
from user.models import NomalUser


class Cart(models.Model):
    user = models.ForeignKey(NomalUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_added) + str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    category_item = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.category_item) + str(self.cart)
