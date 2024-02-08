from django.contrib import admin
from app.models import Item
from .models import Admin, Users, User, Login, Announcement, IncidentReport, Resource, Bill, Payment, Booking

admin.site.register(Item)
admin.site.register(Admin)
admin.site.register(Users)
admin.site.register(Login)
admin.site.register(Announcement)
admin.site.register(IncidentReport)
admin.site.register(Resource)
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(Booking)