from django.urls import path, include

from .views import CommentDetail
from .views import CommentListCreateAPIView


urlpatterns = [
    path('single/<int:pk>/', CommentDetail.as_view(), name='cmt_test_api_sing'),
    path('list/', CommentListCreateAPIView.as_view(), name='cmt_test_api'),
]
