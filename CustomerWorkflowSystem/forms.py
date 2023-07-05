from django import forms
from .models import Customer, FinancialData  # assuming Customer model is in models.py in the same directory



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'date_of_birth']

class UploadFileForm(forms.Form):
    file = forms.FileField()


class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = ['month', 'income', 'expenses']  # Replace these with the actual field names
