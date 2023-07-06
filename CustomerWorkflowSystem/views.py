from django.shortcuts import render, redirect
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import os
import random
from io import BytesIO
from .forms import UploadFileForm, CustomerForm
from .models import Customer, FinancialData
from asgiref.sync import sync_to_async
from threading import Thread

# Get base directory of the project from settings
BASE_DIR = settings.BASE_DIR


# Function to clean currency value (remove unnecessary symbols and convert to float)
def clean_currency_value(value):
    if isinstance(value, str):
        cleaned_value = value.replace('R', '').replace(',', '').replace('\xa0', '').replace(' ', '').strip()
        try:
            return float(cleaned_value)
        except ValueError:
            return None
    return value

# View for capturing customer info
def capture_customer_info(request):
    if request.method == 'POST':
        # Instantiate the form with POST data
        form = CustomerForm(request.POST)
        file_form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid() and file_form.is_valid():
            # Save the customer data and store the file
            customer = form.save()
            uploaded_file = file_form.cleaned_data['file']

            # Define the directory for storing the file
            file_dir = os.path.join(BASE_DIR, 'CustomerWorkflowSystem', 'static', 'img')

            # Create directory if it doesn't exist
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            # Create path for the file
            file_path = os.path.join(file_dir, f'{customer.first_name}_{customer.last_name}.xlsx')

            # Save the uploaded file to the specified path
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Load the data from the Excel file
            df = pd.read_excel(file_path, engine='openpyxl')

            # Create FinancialData objects from the dataframe
            for _, row in df.iterrows():
                income = random.randint(19453, 35593)
                expenses = random.randint(1800, 28543)

                FinancialData.objects.create(
                    customer=customer,
                    month=row['Month'],
                    income=income,
                    expenses=expenses
                )

            # Render and save the graph for this customer
            render_and_save_graph(customer)
            return redirect('render_temporal_graph', customer_id=customer.id)
    else:
        form = CustomerForm()
        file_form = UploadFileForm()

    # Render the form for capturing customer info
    return render(request, 'CustomerWorkflowSystem/capture_customer.html', {'customer_form': form, 'file_form': file_form})

# Function to render and save the graph for a customer
def render_and_save_graph(customer):
    def _render_and_save_graph_async():
        import matplotlib
        matplotlib.use('Agg')  # switch to a non-interactive backend
        import matplotlib.pyplot as plt

        # Query the FinancialData objects for this customer
        financial_data = FinancialData.objects.filter(customer=customer)
        df = pd.DataFrame(list(financial_data.values()))

        # Preprocess the dataframe
        df.columns = df.columns.str.strip().str.lower()
        month_order = list(calendar.month_abbr[1:])
        df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
        df['income'] = df['income'].apply(clean_currency_value)
        df['expenses'] = df['expenses'].apply(clean_currency_value)
        # Sort the dataframe by month
        df.sort_values(by='month', inplace=True)

        # Plot the graph
        plt.figure(figsize=(10, 6))
        plt.bar(df['month'], df['income'], label='Income')
        plt.bar(df['month'], df['expenses'], label='Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Income and Expenses Over Time')
        plt.legend()

        # Define the directory and file path for the graph
        file_dir = os.path.join(BASE_DIR, 'CustomerWorkflowSystem', 'static', 'img')
        file_path = os.path.join(file_dir, 'temporal_graph.png')

        # Create directory if it doesn't exist
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        # Save the graph as a .png file
        with open(file_path, 'wb') as f:
            plt.savefig(f, format='png')

        # Close the plot
        plt.close()

    # Start a new thread to render and save the graph
    thread = Thread(target=_render_and_save_graph_async)
    thread.start()
    return thread # return thread

# View for rendering the temporal graph
def render_temporal_graph(request, customer_id):
    # Fetch the customer by ID
    customer = Customer.objects.get(id=customer_id)

    # Render and save the graph (and wait for it to finish)
    thread = render_and_save_graph(customer)
    thread.join()  # wait for the thread to complete

    # Render the webpage with the graph
    return render(request, 'CustomerWorkflowSystem/render_temporal_graph.html', {'customer': customer})
