from django.urls import path, include

from .views import CategoryDetailView,CategoryListView,CategoryDeleteView
# from .views import products_by_category
from .views import add_category,edit_category

app_name = 'category'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category'),
    path('products/<slug:slug>/',CategoryDetailView.as_view(), name='products_by_category'),

    path('add/', add_category, name='add_category'),
    path('edit/<int:category_id>/', edit_category, name='edit_category'),
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),

    path('api/', include("category.api.urls")),
]
