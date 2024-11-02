from django import forms
from .models import Customer, Purchase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'profile_photo']  # Add other fields as needed

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item_name', 'price', 'is_payment']  # Add other fields as needed

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
