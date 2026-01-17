from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tools, name='tool_list'),
    path('<int:pk>/', views.ToolDetailView.as_view(), name='tool_detail'),
]