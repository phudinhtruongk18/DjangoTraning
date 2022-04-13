from django.urls import path,include
from .views import total

app_name = 'healchecker'

urlpatterns = [
    # path('',  FukuView.as_view(), name="fuk"),
    # path(r'', include('health_check.urls')),
    # path('fuk', test_fuku, name="fuk"),
    path('',  total, name="total"),
]
