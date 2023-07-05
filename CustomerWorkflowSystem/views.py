from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomerForm, FinancialDataForm
from .models import Customer, FinancialData
import pandas as pd



def capture_customer_info(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES)
        if customer_form.is_valid():
            customer = customer_form.save()
            return redirect('render_temporal_graph', customer_id=customer.id)
    else:
        customer_form = CustomerForm()

    return render(request, 'CustomerWorkflowSystem/capture_customer.html', {'customer_form': customer_form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = pd.read_excel(file)
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                customer = customer_form.save()
                for i, row in data.iterrows():
                    FinancialData.objects.create(customer=customer, date=row['date'], income=row['income'], expense=row['expense'])
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def render_temporal_graph(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    financial_data = FinancialData.objects.filter(customer=customer)
    return render(request, 'CustomerWorkflowSystem/render_temporal_graph.html', {'customer': customer, 'financial_data': financial_data})
