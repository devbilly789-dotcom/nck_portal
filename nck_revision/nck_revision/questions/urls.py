from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('admin-panel/questions/', views.manage_questions, name='manage_questions'),
    path('admin-panel/questions/add/', views.add_question, name='add_question'),
    path('admin-panel/questions/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('admin-panel/questions/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('admin-panel/categories/', views.manage_categories, name='manage_categories'),
]
