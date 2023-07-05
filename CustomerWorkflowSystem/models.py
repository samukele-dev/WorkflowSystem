from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FinancialData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenditure = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Financial Data for {self.customer}"
