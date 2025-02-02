from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend the default User model
class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_renter = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    

# Categories model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Tools model
class Tool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    daily_rental_price = models.FloatField()
    condition = models.CharField(max_length=255)
    availability_status = models.BooleanField(default=True)
    images = models.TextField()  # This could store URLs or file paths
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tools')

    def __str__(self):
        return self.name

# Rentals model
class Rental(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='rentals')
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    total_price = models.FloatField()
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Payments model
class Payment(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Reviews model
class Review(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.tool.name}'
