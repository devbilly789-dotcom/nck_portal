from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from datetime import date, timedelta
from .models import CustomUser, Payment

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_approved', 'is_staff']
    list_filter = ['is_approved', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('NCK Info', {'fields': ('phone', 'is_approved')}),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'mpesa_code', 'amount', 'status', 'submitted_at', 'valid_until']
    list_filter = ['status']
    actions = ['approve_payments', 'reject_payments']
    
    def approve_payments(self, request, queryset):
        for payment in queryset.filter(status='pending'):
            payment.status = 'approved'
            payment.approved_at = timezone.now()
            payment.valid_until = date.today() + timedelta(days=30)
            payment.save()
            payment.user.is_approved = True
            payment.user.save()
        self.message_user(request, "Selected payments approved.")
    approve_payments.short_description = "Approve selected payments"
    
    def reject_payments(self, request, queryset):
        queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, "Selected payments rejected.")
    reject_payments.short_description = "Reject selected payments"
