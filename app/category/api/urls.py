from django.urls import path, include

from .views import CategoryDetail
from .views import CategoryListCreateAPIView

from .views import ProductQuantityPerCategory

# app_name = 'categoryapi'

urlpatterns = [
    path('v2/', include('category.api.routers'), name='category_view_set'),
    # API 
    path('single/<int:pk>/', CategoryDetail.as_view(), name='my_category'),
    path('list/', CategoryListCreateAPIView.as_view(), name='category_list'),
    
    path('products_quantity_per_category/', ProductQuantityPerCategory.as_view(), name='products_quantity_per_category'),
]
