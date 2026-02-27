from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from .models import Question
from accounts.models import Payment, UserProfile
from .forms import QuestionForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@admin_required
def admin_dashboard(request):
    total_questions = Question.objects.count()
    total_students = UserProfile.objects.count()
    pending_payments = Payment.objects.filter(status='pending').count()
    active_subscriptions = UserProfile.objects.filter(is_subscription_active=True).count()
    recent_payments = Payment.objects.filter(status='pending').order_by('-submitted_at')[:10]

    return render(request, 'admin_panel/dashboard.html', {
        'total_questions': total_questions,
        'total_students': total_students,
        'pending_payments': pending_payments,
        'active_subscriptions': active_subscriptions,
        'recent_payments': recent_payments,
    })


@admin_required
def manage_payments(request):
    status_filter = request.GET.get('status', 'pending')
    payments = Payment.objects.filter(status=status_filter).order_by('-submitted_at')
    return render(request, 'admin_panel/payments.html', {
        'payments': payments,
        'status_filter': status_filter,
    })


@admin_required
def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            payment.status = 'approved'
            payment.approved_at = timezone.now()
            payment.approved_by = request.user
            payment.save()
            # Activate subscription for 30 days
            profile = payment.user.profile
            profile.is_subscription_active = True
            profile.subscription_expiry = date.today() + timedelta(days=30)
            profile.save()
            messages.success(request, f'Payment approved for {payment.user.username}. Subscription activated for 30 days.')
        elif action == 'reject':
            payment.status = 'rejected'
            payment.notes = request.POST.get('notes', '')
            payment.save()
            messages.warning(request, f'Payment rejected for {payment.user.username}.')
        return redirect('admin_panel:payments')
    return render(request, 'admin_panel/approve_payment.html', {'payment': payment})


@admin_required
def manage_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/questions.html', {'questions': questions})


@admin_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.created_by = request.user
            q.save()
            messages.success(request, 'Question added successfully!')
            if 'add_another' in request.POST:
                return redirect('admin_panel:add_question')
            return redirect('admin_panel:questions')
    else:
        form = QuestionForm()
    return render(request, 'admin_panel/question_form.html', {'form': form, 'action': 'Add'})


@admin_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated!')
            return redirect('admin_panel:questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin_panel/question_form.html', {'form': form, 'action': 'Edit', 'question': question})


@admin_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted.')
        return redirect('admin_panel:questions')
    return render(request, 'admin_panel/delete_question.html', {'question': question})


@admin_required
def manage_students(request):
    profiles = UserProfile.objects.select_related('user').order_by('-user__date_joined')
    return render(request, 'admin_panel/students.html', {'profiles': profiles})
