from django.db import models

# A model to represent a customer
class Customer(models.Model):
    first_name = models.CharField(max_length=100)  # The customer's first name
    last_name = models.CharField(max_length=100)   # The customer's last name
    date_of_birth = models.DateField()              # The customer's date of birth

    def __str__(self):
        # String representation of the customer model
        # Will display as "First Name Last Name" when cast to a string
        return f"{self.first_name} {self.last_name}"

# A model to represent financial data associated with a customer
class FinancialData(models.Model):
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE  # if a Customer object is deleted, all related FinancialData objects will be deleted as well
    )
    month = models.CharField(max_length=3, null=True)  # The month the financial data applies to ('Jan', 'Feb', etc.)
    income = models.DecimalField(max_digits=9, decimal_places=2)  # The customer's income for the month
    expenses = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)  # The customer's expenses for the month. This field is optional.

    def __str__(self):
        # String representation of the financial data model
        # Will display as "Financial Data for First Name Last Name" when cast to a string
        return f"Financial Data for {self.customer}"
