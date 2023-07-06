from django import forms
from .models import Customer, FinancialData  # Importing the Customer and FinancialData models

# CustomerForm is a form associated with the Customer model.
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer  # Specifies that this form is associated with the Customer model
        fields = ['first_name', 'last_name', 'date_of_birth']  # These are the fields we want to include in the form

# UploadFileForm is a generic form not associated with any particular model, 
# used specifically for file upload
class UploadFileForm(forms.Form):
    file = forms.FileField()  # This form contains only one field: a file upload field.

# FinancialDataForm is a form associated with the FinancialData model.
class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData  # Specifies that this form is associated with the FinancialData model
        fields = ['month', 'income', 'expenses']  # These are the fields we want to include in the form
