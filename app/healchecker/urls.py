from django.urls import path,include

app_name = 'healchecker'

urlpatterns = [
    # path('',  FukuView.as_view(), name="fuk"),
    path(r'', include('health_check.urls')),
]
