from django.urls import path  
from .views import CategoryList, CategoryDetail, CategoryListDetailfilter, CreateCategory, EditCategory, AdminCategoryDetail, DeleteCategory
from .views import CategoryListView, CategoryDetailView
from .views import category_list
from .views import add_category,delete_category,edit_category

app_name = 'blog_api'

urlpatterns = [
    # UI

    path('add_category/', add_category, name='add_category'),
    path('edit_category/<int:category_id>', edit_category, name='edit_category'),
    path('delete_category/<int:category_id>', delete_category, name='delete_category'),

    # API 
    path('api/test', category_list, name='api_category_list'),
    path('api/', CategoryList.as_view(), name='api_list_category'),
    path('api/category/<str:pk>/', CategoryDetail.as_view(), name='api_detail_category'),
    path('api/search/', CategoryListDetailfilter.as_view(), name='api_search_category'),

    # category Admin URLs
    path('api/admin/create/', CreateCategory.as_view(), name='api_create_category'),
    path('api/admin/edit/categorydetail/<int:pk>/', AdminCategoryDetail.as_view(), name='api_admindetail_category'),
    path('api/admin/edit/<int:pk>/', EditCategory.as_view(), name='api_edit_category'),
    path('api/admin/delete/<int:pk>/', DeleteCategory.as_view(), name='api_delete_category'),
]
