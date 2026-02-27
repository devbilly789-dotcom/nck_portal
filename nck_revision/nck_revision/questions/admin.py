from django.contrib import admin
from .models import Category, Question

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'course']
    list_filter = ['course']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'difficulty', 'is_active', 'created_at']
    list_filter = ['category__course', 'difficulty', 'is_active']
    search_fields = ['question_text', 'answer']
