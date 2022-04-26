from django.urls import path
from .views import register,login,logout,dashboard,activate
from .views import MyApiRegister
from .views import user_manage_view


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('api_register/', MyApiRegister.as_view(), name="api_register"),

    # valid?
    path('user_manage_view/', user_manage_view, name='user_manage_view'),
]
