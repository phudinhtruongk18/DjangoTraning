from django.urls import path,include
from . import views

app_name = 'healchecker'

urlpatterns = [
    path('',  views.total, name="total"),
]