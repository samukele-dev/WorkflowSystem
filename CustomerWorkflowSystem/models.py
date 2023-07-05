from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

class FinancialData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenditure = models.DecimalField(max_digits=10, decimal_places=2)
