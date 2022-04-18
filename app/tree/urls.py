from django.urls import path,include
from .views import products_by_catalog,CatalogListView,CategoryDetailView,ProductDetailView
from .views import submit_review

urlpatterns = [
    path('', CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>', CategoryDetailView.as_view(), name='products_by_catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
]
