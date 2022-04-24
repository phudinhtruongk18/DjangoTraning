from django.contrib import admin

from .models import Product,ProductInCatalog,Photo
admin.site.register(Product)
admin.site.register(ProductInCatalog)
admin.site.register(Photo)
