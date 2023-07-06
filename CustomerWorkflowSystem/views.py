from django.conf import settings
from django.shortcuts import render, redirect
from .forms import UploadFileForm, CustomerForm, FinancialDataForm
from .models import Customer, FinancialData
import pandas as pd
import matplotlib.pyplot as plt
import calendar


import os

def capture_customer_info(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        file_form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and file_form.is_valid():
            customer = form.save()
            
            # Save the uploaded Excel file to the 'media' directory
            uploaded_file = file_form.cleaned_data['file']
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
        file_form = UploadFileForm()

    return render(request, 'CustomerWorkflowSystem/capture_customer.html', {'customer_form': form, 'file_form': file_form})


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
                    FinancialData.objects.create(
                        customer=customer,
                        month=row['Month'],
                        income=row['Income'],
                        expenses=row['Expenses']
                    )
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# ...

def render_temporal_graph(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    financial_data = FinancialData.objects.filter(customer=customer)

    # Create a DataFrame from the FinancialData query
    df = pd.DataFrame(list(financial_data.values()))

    # Convert column names to lowercase and remove leading/trailing whitespaces
    df.columns = df.columns.str.strip().str.lower()

    # Convert 'month' column to categorical with correct ordering
    month_order = list(calendar.month_abbr[1:])  # ['Jan', 'Feb', 'Mar', ..., 'Dec']
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    # Sort DataFrame by 'month'
    df.sort_values(by='month', inplace=True)
    
    # Print column names
    print(df.columns)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(df['month'], df['income'], label='Income')
    plt.bar(df['month'], df['expenses'], label='Expenses')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Income and Expenses Over Time')
    plt.legend()

    # Specify the path to the static directory in your app
    app_static_dir = os.path.join(settings.BASE_DIR, 'CustomerWorkflowSystem', 'static', 'img')

    # Ensure the directory exists
    os.makedirs(app_static_dir, exist_ok=True)

    # Save the plot
    plt.savefig(os.path.join(app_static_dir, 'temporal_graph.png'))

    return render(request, 'CustomerWorkflowSystem/render_temporal_graph.html', {'customer': customer})
