from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ==========================
# USER PROFILE
# ==========================
class Profile(models.Model):
    USER_TYPE = (
        ('student', 'Student'),
        ('content_admin', 'Content Admin'),
        ('payment_admin', 'Payment Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE,
        default='student'
    )
    subscription_active = models.BooleanField(default=False)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# ==========================
# PAYMENT MODEL
# ==========================
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=20, unique=True)
    approved = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.mpesa_code}"


# ==========================
# QUESTION MODEL
# ==========================
class Question(models.Model):
    CATEGORY = (
        ('BSN', 'BSN'),
        ('KRCHN', 'KRCHN'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY)
    question_text = models.TextField()
    answer_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # <-- fixed for existing rows

    def __str__(self):
        return f"{self.category} Question #{self.id}"