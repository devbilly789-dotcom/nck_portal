from django.urls import path
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('payment/', views.payment_view, name='payment'),

    # Admin URLs
    path('payment-admin/', views.payment_admin_view, name='payment_admin'),
    path('question-upload/', views.question_upload_view, name='question_upload'),

    # Student question list
    path('questions/', views.question_list_view, name='question_list'),
]