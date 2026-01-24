from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tools, name='tool_list'),
    path('<int:pk>/', views.tool_detail, name='tool_detail'),
    path('return/<int:borrowing_id>/', views.return_tool, name='return_tool'),
    path('resolve/<int:borrowing_id>/', views.resolve_dispute, name='resolve_dispute'),
]