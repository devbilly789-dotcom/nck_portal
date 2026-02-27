from django.db import models

class Category(models.Model):
    COURSE_CHOICES = [
        ('BSN', 'Bachelor of Science in Nursing (BSN)'),
        ('KRCHN', 'Kenya Registered Community Health Nurse (KRCHN)'),
    ]
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['course', 'name']
    
    def __str__(self):
        return f"[{self.course}] {self.name}"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(blank=True, help_text="Optional detailed explanation")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'id']
    
    def __str__(self):
        return f"{self.category} - Q{self.id}: {self.question_text[:60]}..."
