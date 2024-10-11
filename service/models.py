from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    vehicle_number = models.CharField(max_length=200)
    running_kilometer = models.PositiveIntegerField()
    work_status_choices =(
        ("pending","pending"),
        ("in_progress","in_progress"),
        ("completed","completed")
    )
        
    
    work_status = models.CharField(max_length=200, choices=work_status_choices,default="pending")
    
    service_advisor = models.ForeignKey(User,on_delete=models.CASCADE)
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Work(models.Model):
    
    customer_object = models.ForeignKey(Customer,on_delete=models.CASCADE)
    
    description = models.CharField(max_length=300)
    
    amount = models.FloatField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)