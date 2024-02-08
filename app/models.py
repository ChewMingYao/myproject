"""
Definition of models.
"""
from django.shortcuts import get_object_or_404
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from datetime import date
from django.forms import ValidationError

#sharing entity

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)

class Login(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username if self.user else "No User"

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    user_name = models.CharField(max_length=255, unique=True)
    room_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    number_access_card = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username if self.user else "No User"

class User(models.Model):
    username = models.CharField(max_length=255)

class Admin(models.Model):
    admin_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
   
class Announcement(models.Model):
    announcement = models.TextField()
    announcement_title = models.CharField(max_length=255)
    announcement_datetime = models.DateTimeField()

class IncidentReport(models.Model):
    description = models.TextField()
    incident_image = models.ImageField(null=True, blank=True, upload_to = 'incident_images/')
    location = models.CharField(max_length=255)
    reported_by = models.CharField(max_length=100)
    incident_date = models.DateField()

class Resource(models.Model):
    resource_name = models.CharField(max_length=255)
    resource_id = models.CharField(max_length=255, unique=True)
    resource_image = models.ImageField(null=True, blank=True, upload_to = 'resource_images/')
    RESOURCE_TYPES=[('Sports','Sports'),('Learning','Learning'),('Entertainment','Entertainment')]
    resource_type = models.CharField(max_length=255, choices=RESOURCE_TYPES)
    RESOURCE_STATUSES = [('Available', 'Available'), ('Unavailable', 'Unavailable'), ('Maintenance', 'Maintenance')]
    resource_status = models.CharField(max_length=100, choices=RESOURCE_STATUSES)
    resource_capacity = models.IntegerField()
    TIME_SLOTS = [
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
    ]

    @staticmethod
    def get_first_time_slots():
        return [slot[0] for slot in Resource.TIME_SLOTS]
    
    def __str__(self):
        return self.resource_name
    
class Booking(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_name', null=True, blank=True)
    resource_fk_id = models.ForeignKey(Resource, on_delete=models.CASCADE, to_field='resource_id', null=True)
    date = models.DateField()
    time_slot = MultiSelectField(choices=Resource.TIME_SLOTS, max_choices=12, max_length=60, null=True, blank=True)
    date_string = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        resource_name_instance = self.resource_fk_id
        return f"{self.user.user_name} booked {resource_name_instance.resource_name} on {self.date} at {', '.join(self.time_slot)}"

    def save(self, *args, **kwargs):
        # Always update date_string with the current string representation of date
        self.date_string = self.date.strftime("%b. %#d, %Y")

        super().save(*args, **kwargs)

    def get_user_name(self):
        return self.user.user_name if self.user else None



class Bill(models.Model):
    bill_id = models.CharField(primary_key=True, max_length=10)
    due_date = models.DateField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        user_name = self.get_user_name() if self.user else 'N/A'
        return f"Bill {self.bill_id} for User {user_name}"

    def get_user_name(self):
        return self.user.user_name if self.user else None
    
class Payment(models.Model):
    BILL_TYPE = [('ELECTRIC', 'ELECTRIC'), ('WATER', 'WATER'), ('WIFI', 'WIFI'), ('RENTAL', 'RENTAL'),('MAINTAINENCE','MAINTAINENCE')]
    bill_type = models.CharField(max_length=100, choices = BILL_TYPE)    
    recipient_name = models.TextField()
    total_payment = models.FloatField()
    payment_amount = models.FloatField()
    account_number = models.TextField()
    card_type = models.TextField()
    remark = models.TextField()
    payment_date = models.DateField(null=True) 
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    transaction_status = models.CharField(max_length=20, default='Pending')

    def calculate_transaction_status(self):
        if self.payment_amount == 0:
            return 'Not Paid Yet'
        elif self.total_payment > 0:
            return 'Insufficient'
        elif self.total_payment == 0:
            return 'Successful'
        else:
            return 'Error'

    def save(self, *args, **kwargs):
        self.total_payment -= self.payment_amount
        self.transaction_status = self.calculate_transaction_status()
        super().save(*args, **kwargs)
        

        

    