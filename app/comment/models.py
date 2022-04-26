from django.db import models
from product.models import Product
from user.models import NomalUser


class Comment(models.Model):
    """Only allow user can have oen comment for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(NomalUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.product}-{self.created_at}"
