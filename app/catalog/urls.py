from django.urls import path  
from .views import CatalogList, CatalogDetail, CatalogListDetailfilter, CreateCatalog, EditCatalog, AdminCatalogDetail, DeleteCatalog
from .views import CatalogListView, CatalogDetailView
from .views import catalog_list
from .views import add_catalog,delete_catalog,edit_catalog

app_name = 'blog_api'

urlpatterns = [
    # UI
    path('', CatalogListView.as_view(), name='catalog'),

    path('catalog/<slug:slug>', CatalogDetailView.as_view(), name='products_by_catalog'),
    path('add_catalog/', add_catalog, name='add_catalog'),
    path('edit_catalog/<int:catalog_id>', edit_catalog, name='edit_catalog'),
    path('delete_catalog/<int:catalog_id>', delete_catalog, name='delete_catalog'),

    # API 
    path('api/test', catalog_list, name='api_catalog_list'),
    path('api/', CatalogList.as_view(), name='api_list_catalog'),
    path('api/catalog/<str:pk>/', CatalogDetail.as_view(), name='api_detail_catalog'),
    path('api/search/', CatalogListDetailfilter.as_view(), name='api_search_catalog'),

    # Catalog Admin URLs
    path('api/admin/create/', CreateCatalog.as_view(), name='api_create_catalog'),
    path('api/admin/edit/catalogdetail/<int:pk>/', AdminCatalogDetail.as_view(), name='api_admindetail_catalog'),
    path('api/admin/edit/<int:pk>/', EditCatalog.as_view(), name='api_edit_catalog'),
    path('api/admin/delete/<int:pk>/', DeleteCatalog.as_view(), name='api_delete_catalog'),
]
