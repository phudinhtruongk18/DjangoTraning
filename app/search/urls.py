from django.urls import path, include


urlpatterns = [
    path('api/', include('search.api.urls')),
]
