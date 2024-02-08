"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm 
from .models import Users, Login, IncidentReport, Resource, Announcement, Bill, Payment, Admin, Booking


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['userid'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'userid', 
            'id':'userid', 
            'type':'text', 
            'placeholder':'Chew8804', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'Password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Confirm Password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'Chew Ming Yao', 
            'maxlength': '30', 
            'minlength': '6', 
            }) 
        self.fields['room_number'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'room_number', 
            'id':'room_number', 
            'type':'text', 
            'placeholder':'J-17-16', 
            'maxlength': '10', 
            'minlength': '7', 
            }) 
        self.fields['phone_number'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'phone_number', 
            'id':'phone_number', 
            'type':'text', 
            'placeholder':'01120718079', 
            'maxlength': '11', 
            'minlength': '10', 
            }) 
        self.fields['number_access_card'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'number_access_card', 
            'id':'number_access_card', 
            'type':'int', 
            'placeholder':'1', 
            }) 
 
    userid = forms.CharField(max_length=16) 
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    username = forms.CharField(max_length=30)
    room_number = forms.CharField(max_length=10)
    phone_number = forms.CharField(max_length=11)
    number_access_card = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'room_number', 'phone_number', 'number_access_card')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']

        if commit:
            user.save()

            login_instance = Login(user=user, password=self.cleaned_data['password1'])
            login_instance.save()

            users_instance = Users(
                user=user,
                user_name=self.cleaned_data['username'],
                room_number=self.cleaned_data['room_number'],
                phone_number=self.cleaned_data['phone_number'],
                number_access_card=self.cleaned_data['number_access_card']
            )
            users_instance.save()

        return user
    
class IncidentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['description'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'description', 
            'id':'description', 
            'type':'text', 
            'placeholder':'Enter description here',  
            }) 
        self.fields['incident_image'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'incident_image', 
            'id':'incident_image', 
            'type':'image', 
            'placeholder':'Upload image', 
            }) 
        self.fields['location'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'location', 
            'id':'location', 
            'type':'text', 
            'placeholder':'Enter Incident Location', 
            'maxlength':'30',  
            'minlength':'1' 
            }) 
        self.fields['reported_by'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'reported_by', 
            'id':'reported_by', 
            'type':'text', 
            'placeholder':'Chew Ming Yao', 
            'maxlength': '30', 
            'minlength': '1', 
            })         
        self.fields['incident_date'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'incident_date', 
            'id':'incident_date', 
            'type':'date', 
            'placeholder':'YYYY-MM-DD', 
            'maxlength': '10', 
            'minlength': '10', 
            }) 
 
    description = forms.Textarea()
    incident_image = forms.ImageField()
    location = forms.CharField()
    reported_by = forms.CharField(max_length=30, label=False) 
    incident_date = forms.DateField()

    class Meta:
        model = IncidentReport
        fields = ('description', 'incident_image', 'location', 'reported_by', 'incident_date')

    def save(self, commit=True):
            user = super().save(commit=False)

            if commit:
                user.save()
                
            return user

class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['resource_name'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_name', 
            'id':'resource_name', 
            'type':'text', 
            'placeholder':'Enter Resource Name',  
            }) 
        self.fields['resource_id'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_id', 
            'id':'resource_id', 
            'type':'text', 
            'placeholder':'Enter Resource ID', 
            }) 
        self.fields['resource_image'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_image', 
            'id':'resource_image', 
            'type':'image', 
            'placeholder':'Upload image', 
            }) 
        self.fields['resource_type'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_type', 
            'id':'resource_type', 
            'type':'text', 
            'placeholder':'Enter Resource Type', 
            'maxlength':'30',  
            'minlength':'1' 
            }) 
        self.fields['resource_status'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_status', 
            'id':'resource_status', 
            'placeholder':'Enter Resource Type', 
            'maxlength': '30', 
            'minlength': '1', 
            })       
        self.fields['resource_capacity'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'resource_capacity', 
            'id':'resource_capacity', 
            'type':'integer',  
            'placeholder':'1', 
            }) 


    resource_name = forms.CharField(max_length=255)
    resource_id = forms.CharField(max_length=255)
    resource_image = forms.ImageField()
    RESOURCE_TYPES=[('Sports','Sports'),('Learning','Learning'),('Entertainment','Entertainment')]
    resource_type = forms.ChoiceField(choices=RESOURCE_TYPES)
    RESOURCE_STATUSES = [('Available', 'Available'), ('Unavailable', 'Unavailable'), ('Maintenance', 'Maintenance')]
    resource_status = forms.ChoiceField(choices=RESOURCE_STATUSES)
    resource_capacity = forms.IntegerField()

    class Meta:
        model = Resource
        fields = ('resource_name', 'resource_id', 'resource_image', 'resource_type', 'resource_status', 'resource_capacity')
    
    def save(self, commit=True):
            user = super().save(commit=False)

            if commit:
                user.save()
                
            return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time_slot']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        
        self.fields['date'].widget.attrs.update({'id': 'datepicker', 'class': 'datepicker'})
        self.fields['date'].input_formats = ['%Y-%m-%d']
        self.fields['time_slot'].widget = forms.CheckboxSelectMultiple(choices=Resource.TIME_SLOTS)  
        self.fields['time_slot'].required = False



class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['announcement'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'announcement', 
            'id':'announcement', 
            'type':'text', 
            'placeholder':'Enter announcement here',  
            })
        self.fields['announcement_title'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'announcement_title', 
            'id':'announcement_title', 
            'type':'text', 
            'placeholder':'Title', 
            }) 
        self.fields['announcement_datetime'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'announcement_datetime', 
            'id':'announcement_datetime', 
            'type':'datetime-local', 
            'placeholder':'YYYY-MM-DD HH:MM',
            }) 
        
    announcement = forms.Textarea()
    announcement_title = forms.CharField()
    announcement_datetime = forms.DateTimeField()

    class Meta:
        model = Announcement
        fields = ('announcement', 'announcement_title', 'announcement_datetime')

    def save(self, commit=True):
            user = super().save(commit=False)

            if commit:
                user.save()
                
            return user

class BillAssignForm(forms.ModelForm):
    bill_id = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '#B001'}))
    user = forms.ModelChoiceField(queryset=Users.objects.all())
    due_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    BILL_TYPE = [('ELECTRIC', 'ELECTRIC'), ('WATER', 'WATER'), ('WIFI', 'WIFI'), ('RENTAL', 'RENTAL'),('MAINTAINENCE','MAINTAINENCE')]
    bill_type = forms.ChoiceField(choices = BILL_TYPE)
    total_payment = forms.FloatField()
    
    class Meta:
        model = Bill
        fields = ('bill_id', 'user', 'due_date', 'bill_type', 'total_payment')
    
    def save(self, commit=True):
        bill = super().save(commit=False)

        if commit:
            bill.save()

            payment_instance = Payment(
                bill_type=self.cleaned_data['bill_type'],
                recipient_name='',
                total_payment=self.cleaned_data['total_payment'], 
                payment_amount=0.0,
                account_number='',
                card_type='',
                remark='',
                payment_date=None,
                transaction_status='Not Paid Yet',
                bill=bill,
            )
            payment_instance.save()

        return bill

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['room_number', 'phone_number', 'number_access_card']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['phone_number']

class PaymentForm(forms.ModelForm):
    bill_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    bill_type = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    total_payment = forms.FloatField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
    recipient_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Recipient Name'}))
    payment_amount = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Payment Amount'}))
    account_number = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Account Number'}))
    card_type = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Card Type'}))
    remark = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Remark'}))
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
        
    class Meta:
        model = Payment
        fields = ['bill_id', 'bill_type', 'total_payment', 'recipient_name', 'payment_amount', 'account_number', 'card_type', 'remark', 'payment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['recipient_name', 'payment_amount', 'account_number', 'card_type', 'remark', 'payment_date']:
            self.fields[field_name].widget.attrs.pop('readonly', None)

    def save(self, commit=True):
        payment = super().save(commit=False)

        if commit:
            payment.save()

        return payment

class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resource_name', 'resource_id', 'resource_type', 'resource_status','resource_capacity']

