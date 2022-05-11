from django.urls import path, include

from .views import SearchCategoryListView

urlpatterns = [
    path('category/', SearchCategoryListView.as_view(), name='search-category-list'),
]
