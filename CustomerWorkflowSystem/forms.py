from django import forms
from .models import Customer, FinancialData

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'date_of_birth']

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['date', 'income', 'expenditure']
