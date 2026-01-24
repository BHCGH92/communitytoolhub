from django.urls import path
from . import views

urlpatterns = [
path('', views.all_tools, name='tool_list'),
    path('<int:pk>/', views.tool_detail, name='tool_detail'),
    path('checkout/<int:tool_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('return/<int:borrowing_id>/', views.return_tool, name='return_tool'),
    path('resolve/<int:borrowing_id>/', views.resolve_dispute, name='resolve_dispute'),
]