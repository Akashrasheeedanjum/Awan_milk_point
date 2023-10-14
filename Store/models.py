from django.contrib.auth.models import AbstractUser
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',
    )

    # Additional fields for user signups
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Add a ForeignKey to associate users with a branch
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def __str__(self):
        return self.username

class MilkCenter(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.SET_DEFAULT, default=1)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    price_of_milk = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    opening_balance=models.DecimalField(max_digits=10, decimal_places=2 , default=0.00)
    closing_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return self.name

class Customer(models.Model):
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    opening_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    closing_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)


    def __str__(self):
        return self.name





class MilkPurchase(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    milk_center = models.ForeignKey(MilkCenter, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_liter = models.DecimalField(max_digits=10, decimal_places=2)
    LR = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    Fat = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    SNF = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    price_on_TS = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.milk_center} - {self.purchase_date}"

class MilkSale(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_liter = models.DecimalField(max_digits=10, decimal_places=2)
    LR = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    Fat = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    SNF = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    price_on_TS = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.purchase_date}"

class MakePayment(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    milk_center = models.ForeignKey(MilkCenter, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    payment_datetime = models.DateTimeField(auto_now_add=True)
    balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return f"Payment #{self.id} - {self.amount}"

class ReceivedPayment(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    received_datetime = models.DateTimeField(auto_now_add=True)
    balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    def __str__(self):
        return f"Received Payment #{self.id} - {self.customer} - {self.amount_received}"

class Storage(models.Model):  # Changed "Stor" to "Storage"
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    milk_storage = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    expense = models.DecimalField(max_digits=100, decimal_places=2, null=True)

    def __str__(self):
        return 'Storage'

class Expence(models.Model):  # Changed "Expence" to "Expense"
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    expense_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.expense_name

class CustomerExpence(models.Model):  # Changed "CustomerExpence" to "CustomerExpense"
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    expense_type = models.TextField(blank=True, null=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.customer.name


class Employee(models.Model):
    USER_TYPE_CHOICES = [
        ('supplier', 'Supplier'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        
    ]

    Employee_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',
    )

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    opening_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    closing_balance=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)


    def __str__(self):
        return self.name
