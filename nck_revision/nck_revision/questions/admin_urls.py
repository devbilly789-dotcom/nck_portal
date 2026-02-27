from django.urls import path
from .admin_views import (
    admin_dashboard, manage_payments, approve_payment,
    manage_questions, add_question, edit_question, delete_question,
    manage_students
)

app_name = 'admin_panel'

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('payments/', manage_payments, name='payments'),
    path('payments/<int:payment_id>/approve/', approve_payment, name='approve_payment'),
    path('questions/', manage_questions, name='questions'),
    path('questions/add/', add_question, name='add_question'),
    path('questions/<int:question_id>/edit/', edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', delete_question, name='delete_question'),
    path('students/', manage_students, name='students'),
]
