from django.urls import path, include

from .views import ProductDetailAPIView,PhotoDetailAPIView,CreatePhotoApiView
from .views import ProductCreateAPIView,ProductListAPIView
from .views import CommentProductListAPIView
from .views import get_report_product_list


urlpatterns = [
    path('create_photo/', CreatePhotoApiView.as_view(), name='create_product_photo'),
    path('single_photo/<int:pk>/', PhotoDetailAPIView.as_view(), name='product_photo'),
    path('single/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('create/', ProductCreateAPIView.as_view(), name='products'),
    path('list/', ProductListAPIView.as_view(), name='products'),
    path('report_product/', get_report_product_list, name='report_product'),
    path('comments_of_product/<int:pk>/', CommentProductListAPIView.as_view(), name='comments_of_product'),
]
