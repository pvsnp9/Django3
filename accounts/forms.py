from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  #['customer', 'product']
        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.fields.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.fields.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={'placeholder': 'Email'}),
            # 'password1': forms.PasswordInput(attrs={'placeholder': 'Passwod'}),
            # 'password2': forms.fields.TextInput(attrs={'placeholder': 'Confirm Password'})
        }