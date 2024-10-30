from django import forms
from .models import Customer, Purchase

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['item_name', 'price']
