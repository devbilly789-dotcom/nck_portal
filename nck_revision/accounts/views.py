from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from .forms import RegisterForm, LoginForm, PaymentForm
from .models import Payment

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Please complete your subscription.')
            return redirect('payment')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_panel')
            if user.is_approved:
                return redirect('home')
            return redirect('payment')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def payment_view(request):
    if request.user.is_staff:
        return redirect('admin_panel')
    if request.user.is_approved:
        return redirect('home')
    
    pending = Payment.objects.filter(user=request.user, status='pending').first()
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['mpesa_code'].upper()
            if Payment.objects.filter(mpesa_code=code).exists():
                messages.error(request, 'This M-PESA code has already been used.')
            else:
                payment = form.save(commit=False)
                payment.user = request.user
                payment.mpesa_code = code
                payment.save()
                messages.success(request, 'Payment submitted! Awaiting admin approval.')
                return redirect('payment')
    else:
        form = PaymentForm()
    
    return render(request, 'accounts/payment.html', {'form': form, 'pending': pending})

@login_required
def check_approval(request):
    """AJAX endpoint to check approval status"""
    import json
    from django.http import JsonResponse
    user = request.user
    # refresh from db
    user.refresh_from_db()
    return JsonResponse({'approved': user.is_approved})
