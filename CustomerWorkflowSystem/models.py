from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FinancialData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    month = models.CharField(max_length=3, null=True) # 'Jan', 'Feb', etc.
    income = models.DecimalField(max_digits=9, decimal_places=2) # '20860.00', etc.
    expenses = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True) # '8895.00', etc.


    def __str__(self):
        return f"Financial Data for {self.customer}"
