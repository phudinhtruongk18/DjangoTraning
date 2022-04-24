from django.urls import path,include
from .views import add_product,edit_product,delete_product
from .views import ProductDetailView

from .views import delete_photo

urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('add_product/', add_product, name='add_product'),
    path('add_product/<int:product_id>', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),

    path('delete_photo/<int:photo_id>', delete_photo, name='delete_photo'),
]
