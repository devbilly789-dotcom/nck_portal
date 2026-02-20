from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import RegisterForm
from .models import Payment, Profile, Question


# ==========================
# HELPER FUNCTIONS
# ==========================
def is_content_admin(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'content_admin'


def is_payment_admin(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'payment_admin'


# ==========================
# AUTHENTICATION
# ==========================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registered successfully!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================
# DASHBOARD
# ==========================
@login_required
def dashboard_view(request):
    profile = request.user.profile

    # Auto-expire subscription if past end date
    if profile.subscription_end and profile.subscription_end < timezone.now():
        profile.subscription_active = False
        profile.subscription_start = None
        profile.subscription_end = None
        profile.save()

    return render(request, 'dashboard.html', {'profile': profile})


# ==========================
# PAYMENT SUBMISSION (STUDENT)
# ==========================
@login_required
def payment_view(request):
    profile = request.user.profile

    # Already active subscription
    if profile.subscription_active:
        messages.info(request, "Your subscription is already active.")
        return redirect('dashboard')

    existing_payment = Payment.objects.filter(
        student=request.user,
        approved=False
    ).first()

    if request.method == 'POST':
        mpesa_code = request.POST.get('mpesa_code')

        if existing_payment:
            messages.error(request, "You already submitted a payment. Await approval.")
        else:
            # Prevent duplicate mpesa_code
            if Payment.objects.filter(mpesa_code=mpesa_code).exists():
                messages.error(request, "This M-Pesa code has already been used.")
            else:
                Payment.objects.create(
                    student=request.user,
                    mpesa_code=mpesa_code
                )
                messages.success(request, "Payment submitted successfully. Await admin approval.")
                return redirect('dashboard')

    return render(request, 'payment.html', {'existing_payment': existing_payment})


# ==========================
# ADMIN APPROVAL (PAYMENT ADMIN)
# ==========================
@login_required
@user_passes_test(is_payment_admin)
def payment_admin_view(request):
    # Show all pending payments
    payments = Payment.objects.filter(approved=False)

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id)

            # Approve payment
            payment.approved = True
            payment.save()

            # Activate subscription for student 30 days
            profile = payment.student.profile
            profile.subscription_active = True
            profile.subscription_start = timezone.now()
            profile.subscription_end = timezone.now() + timedelta(days=30)
            profile.save()

            messages.success(request, f"Payment approved for {payment.student.username}")
            return redirect('payment_admin')
        except Payment.DoesNotExist:
            messages.error(request, "Payment not found.")

    return render(request, 'payment_admin.html', {'payments': payments})


# ==========================
# CONTENT ADMIN: QUESTION UPLOAD
# ==========================
@login_required
@user_passes_test(is_content_admin)
def question_upload_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        question_text = request.POST.get('question_text')
        answer_text = request.POST.get('answer_text')

        Question.objects.create(
            category=category,
            question_text=question_text,
            answer_text=answer_text
        )
        messages.success(request, "Question added successfully!")
        return redirect('question_upload')

    return render(request, 'question_upload.html')


# ==========================
# STUDENT: VIEW QUESTIONS
# ==========================
@login_required
def question_list_view(request):
    profile = request.user.profile

    if not profile.subscription_active:
        messages.error(request, "You must pay subscription to view questions.")
        return redirect('dashboard')

    category = request.GET.get('category', 'BSN')
    questions = Question.objects.filter(category=category)

    return render(request, 'question_list.html', {'questions': questions, 'category': category})