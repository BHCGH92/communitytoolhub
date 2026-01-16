from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tools, name='all_tools'),
]