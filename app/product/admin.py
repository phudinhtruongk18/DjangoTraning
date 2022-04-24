from django.contrib import admin

from .models import Product,ProductInCategory,Photo
admin.site.register(Product)
admin.site.register(ProductInCategory)
admin.site.register(Photo)
