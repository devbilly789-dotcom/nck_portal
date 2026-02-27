from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Category, Question
from .forms import QuestionForm, CategoryForm
from accounts.models import Payment

def is_admin(user):
    return user.is_staff

def approved_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        if not request.user.is_approved:
            return redirect('payment')
        return view_func(request, *args, **kwargs)
    return wrapper

@approved_required
def home(request):
    bsn_cats = Category.objects.filter(course='BSN')
    krchn_cats = Category.objects.filter(course='KRCHN')
    selected_course = request.GET.get('course', 'BSN')
    selected_cat = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    questions = Question.objects.filter(is_active=True)
    
    if selected_course:
        questions = questions.filter(category__course=selected_course)
    if selected_cat:
        questions = questions.filter(category_id=selected_cat)
    if search:
        questions = questions.filter(
            Q(question_text__icontains=search) | Q(answer__icontains=search)
        )
    
    categories = Category.objects.filter(course=selected_course)
    
    return render(request, 'questions/home.html', {
        'questions': questions,
        'bsn_cats': bsn_cats,
        'krchn_cats': krchn_cats,
        'categories': categories,
        'selected_course': selected_course,
        'selected_cat': selected_cat,
        'search': search,
    })

# Admin panel views
@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    pending_payments = Payment.objects.filter(status='pending').select_related('user')
    total_questions = Question.objects.count()
    total_users = Payment.objects.filter(status='approved').values('user').distinct().count()
    return render(request, 'admin_panel/dashboard.html', {
        'pending_payments': pending_payments,
        'total_questions': total_questions,
        'total_users': total_users,
    })

@login_required
@user_passes_test(is_admin)
def approve_payment(request, payment_id):
    from django.utils import timezone
    from datetime import date, timedelta
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            payment.status = 'approved'
            payment.approved_at = timezone.now()
            payment.valid_until = date.today() + timedelta(days=30)
            payment.save()
            payment.user.is_approved = True
            payment.user.save()
            messages.success(request, f'{payment.user.username} approved successfully!')
        elif action == 'reject':
            payment.status = 'rejected'
            payment.save()
            messages.warning(request, f'Payment rejected.')
    return redirect('admin_panel')

@login_required
@user_passes_test(is_admin)
def manage_questions(request):
    questions = Question.objects.select_related('category').all()
    course_filter = request.GET.get('course', '')
    if course_filter:
        questions = questions.filter(category__course=course_filter)
    return render(request, 'admin_panel/questions.html', {'questions': questions, 'course_filter': course_filter})

@login_required
@user_passes_test(is_admin)
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question added successfully!')
            return redirect('manage_questions')
    else:
        form = QuestionForm()
    return render(request, 'admin_panel/question_form.html', {'form': form, 'title': 'Add Question'})

@login_required
@user_passes_test(is_admin)
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated!')
            return redirect('manage_questions')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin_panel/question_form.html', {'form': form, 'title': 'Edit Question'})

@login_required
@user_passes_test(is_admin)
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted.')
    return redirect('manage_questions')

@login_required
@user_passes_test(is_admin)
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {'form': form, 'categories': categories})
