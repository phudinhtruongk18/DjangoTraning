from django.urls import path, include

from .views import CategoryDetail
from .views import CategoryListCreateAPIView
from .views import products_quantity_per_category

urlpatterns = [
    path('v2/', include('category.api.routers'), name='test_api_v2'),
    # API 
    path('single/<int:pk>/', CategoryDetail.as_view(), name='test_api_sing'),
    path('list/', CategoryListCreateAPIView.as_view(), name='test_api'),
    path('products_quantity_per_category/', products_quantity_per_category, name='products_quantity_per_category'),
    # path('api/', CategoryList.as_view(), name='api_list_category'),
    # path('api/category/<str:pk>/', CategoryDetail.as_view(), name='api_detail_category'),
    # path('api/search/', CategoryListDetailfilter.as_view(), name='api_search_category'),

    # # category Admin URLs
    # path('api/admin/create/', CreateCategory.as_view(), name='api_create_category'),
    # path('api/admin/edit/categorydetail/<int:pk>/', AdminCategoryDetail.as_view(), name='api_admindetail_category'),
    # path('api/admin/edit/<int:pk>/', EditCategory.as_view(), name='api_edit_category'),
    # path('api/admin/delete/<int:pk>/', DeleteCategory.as_view(), name='api_delete_category'),
]
