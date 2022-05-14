from django.urls import path, include

from .views import ProductDetail,PhotoDetail
from .views import ProductListCreateAPIView
from .views import ReportProductListAPIView,CommentProductListAPIView


urlpatterns = [
    path('single_photo/<int:pk>/', PhotoDetail.as_view(), name='product_photo'),
    path('single/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('list/', ProductListCreateAPIView.as_view(), name='products'),
    path('report_product/', ReportProductListAPIView.as_view(), name='report_product'),
    path('comments_of_product/<int:pk>/', CommentProductListAPIView.as_view(), name='comments_of_product'),
]
