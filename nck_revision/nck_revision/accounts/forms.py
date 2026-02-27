from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Payment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True, help_text="e.g. 07XXXXXXXX")
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['mpesa_code']
        widgets = {
            'mpesa_code': forms.TextInput(attrs={
                'placeholder': 'e.g. QHG7XXXXXXX',
                'maxlength': '20',
                'style': 'text-transform:uppercase'
            })
        }
        labels = {
            'mpesa_code': 'M-PESA Transaction Code'
        }
