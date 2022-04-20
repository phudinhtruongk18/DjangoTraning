from django.urls import path,include
from .views import products_by_catalog,CatalogListView,CategoryDetailView,ProductDetailView
from .views import user_manage_view
from .views import submit_comment, delete_comment
from .views import add_product,edit_product
from .views import delete_photo

urlpatterns = [
    path('', CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>', CategoryDetailView.as_view(), name='products_by_catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('submit_comment/<int:product_id>/', submit_comment, name='submit_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('user_manage_view/', user_manage_view, name='user_manage_view'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>', edit_product, name='edit_product'),
    path('delete_photo/<int:photo_id>', delete_photo, name='delete_photo'),

]
