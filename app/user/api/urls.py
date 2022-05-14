from django.urls import path
from .views import MyApiRegister
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', MyApiRegister.as_view(), name="api_register"),
    path('token/', obtain_auth_token),

]
