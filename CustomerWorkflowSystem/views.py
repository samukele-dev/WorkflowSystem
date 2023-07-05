from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomerForm, FinancialDataForm
from .models import Customer, FinancialData
import pandas as pd
import matplotlib.pyplot as plt

import os

def capture_customer_info(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save()
            
            # Save the uploaded Excel file to the 'media' directory
            uploaded_file = request.FILES['financial_data']
            file_dir = 'media/financial_data_files/'
            file_path = '{}{}_{}.xlsx'.format(file_dir, customer.first_name, customer.last_name)
            
            # Check if the directory exists, if not, create it
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Read the Excel file into a pandas DataFrame and save it to the database
            df = pd.read_excel(file_path)
            for i, row in df.iterrows():
                FinancialData.objects.create(
                    customer=customer,
                    month=row['Month'],
                    income=row['Income'],
                    expenses=row['Expenses']
                )
            
        return redirect('render_temporal_graph', customer_id=customer.id)
    
    else:
        form = CustomerForm()
    return render(request, 'CustomerWorkflowSystem/capture_customer.html', {'customer_form': form})


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

    # Create a DataFrame from the FinancialData query
    df = pd.DataFrame(list(financial_data.values()))

    # Convert 'month' to numeric format
    df['month'] = pd.to_datetime(df['month'], format='%b', errors='coerce').dt.month

    # Sort DataFrame by 'month'
    df.sort_values(by='month', inplace=True)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['month'], df['income'], label='Income')
    plt.plot(df['month'], df['expenses'], label='Expenses')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Income and Expenses Over Time')
    plt.legend()
    plt.savefig(os.path.join(settings.STATIC_ROOT, 'images/temporal_graph.png'))

    return render(request, 'CustomerWorkflowSystem/render_temporal_graph.html', {'customer': customer})
