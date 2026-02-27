from django import forms
from .models import Question, Category

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question_text', 'answer', 'explanation', 'difficulty', 'is_active']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4}),
            'answer': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'course', 'description']
