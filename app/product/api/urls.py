from django.urls import path, include

from .views import ProductDetail,PhotoDetail
from .views import ProductListCreateAPIView


urlpatterns = [
    path('single_photo/<int:pk>/', PhotoDetail.as_view(), name='pro_photo'),
    path('single/<int:pk>/', ProductDetail.as_view(), name='pro_test_api_sing'),
    path('list/', ProductListCreateAPIView.as_view(), name='pro_test_api'),
]
