from django.shortcuts import render, redirect
from .forms import CustomerForm, FinancialDataForm
from .models import Customer, FinancialData

def capture_customer_info(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        financial_data_form = FinancialDataForm(request.POST, request.FILES)
        if customer_form.is_valid() and financial_data_form.is_valid():
            customer = customer_form.save()
            financial_data = financial_data_form.save(commit=False)
            financial_data.customer = customer
            financial_data.save()
            return redirect('temporal_graph', customer_id=customer.id)
    else:
        customer_form = CustomerForm()
        financial_data_form = FinancialDataForm()
    return render(request, 'workflow/capture_customer.html', {'customer_form': customer_form, 'financial_data_form': financial_data_form})
