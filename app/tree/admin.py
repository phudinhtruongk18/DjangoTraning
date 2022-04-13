from django.contrib import admin
from .models import Product, Catalog,ProductInCatalog,Photo
# Register your models here.
admin.site.register(Product)
admin.site.register(Catalog)
admin.site.register(ProductInCatalog)
admin.site.register(Photo)
