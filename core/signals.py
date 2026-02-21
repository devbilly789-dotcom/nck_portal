from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Profile, Payment


# ==========================
# CREATE PROFILE AUTOMATICALLY
# ==========================
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# ==========================
# ACTIVATE SUBSCRIPTION WHEN PAYMENT IS APPROVED
# ==========================
@receiver(post_save, sender=Payment)
def activate_subscription(sender, instance, created, **kwargs):

    # Only activate if payment is approved
    # AND subscription is not already active
    if instance.approved:
        profile = instance.student.profile

        if not profile.subscription_active:
            profile.subscription_active = True
            profile.subscription_start = timezone.now()
            profile.subscription_end = timezone.now() + timedelta(days=30)
            profile.save()
