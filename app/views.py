from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404

from .models import IncidentReport, Bill, Payment, Resource, Users, Announcement, Admin, Booking

from django.contrib.auth import login, authenticate
from .forms import SignUpForm, IncidentForm, ResourceForm, AnnouncementForm, BillAssignForm, UsersForm, PaymentForm, AdminForm, BookingForm, ResourcesForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db.models import Q

# Create your views here.
from django.db.models import F
from django.http import HttpRequest, HttpResponseBadRequest
from django.template import RequestContext 
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from app import models
from django.contrib import messages
from django.shortcuts import render

def home(request):
    """Renders the home page."""
    announcements = Announcement.objects.all().order_by('-announcement_datetime')
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
                'announcements': announcements,
            }
        )

def sign_up(request): 
    if request.method == "POST":
        form = SignUpForm(request.POST) 
        if form.is_valid():
            user = form.save()

            user.username = form.cleaned_data.get('userid')
            user.room_number = form.cleaned_data.get('room_number')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.number_access_card = form.cleaned_data.get('number_access_card')

            user.save()

            user_group = Group.objects.get(name='user')
            user.groups.add(user_group)

            userid = form.cleaned_data.get('userid') 
            password = form.cleaned_data.get('password1')
            
            authenticated_user = authenticate(request, username=userid, password=password)

            if authenticated_user:
                login(request, authenticated_user)
                return redirect('/menu')
    else:
        form = SignUpForm()

    return render(
        request, 
        'app/sign_up.html',
        {
            'title':'Sign Up',
            'year':datetime.now().year,
            'form': form,
        }
    ) 

def resources_entertainment(request):
    """Renders the resources page."""
    resources = Resource.objects.filter(resource_type='Entertainment').order_by('resource_id')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources_entertainment.html',
        {
            'title':'Entertainmnet',
            'resources': resources,
            'year':datetime.now().year,
            'date_now': datetime.now().date,
        }
    )

def resources_learning(request):
    """Renders the resources page."""
    resources = Resource.objects.filter(resource_type='Learning').order_by('resource_id')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources_learning.html',
        {
            'title':'Learning',
            'resources': resources,
            'year':datetime.now().year,
            'date_now': datetime.now().date,
        }
    )

def resources_sports(request):
    """Renders the resources page."""
    resources = Resource.objects.filter(resource_type='Sports').order_by('resource_id')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources_sports.html',
        {
            'title':'Sports',
            'resources': resources,
            'year':datetime.now().year,
            'date_now': datetime.now().date,
        }
    )

def resources_booking(request, id, date):
    """Renders the resources page."""
    resource_check = get_object_or_404(Resource, resource_id=id)

    bookings = Booking.objects.filter(resource_fk_id=resource_check)
    resources = Resource.objects.filter(resource_id=id)
    bookings = Booking.objects.filter(resource_fk_id=id)
    selected_date = datetime.strptime(date, "%Y-%m-%d").strftime("%b. %#d, %Y")
    date_type = datetime.strptime(selected_date, "%b. %d, %Y")
    users = get_object_or_404(Users, user=request.user)
    all_time_slots = Resource.objects.get(resource_id=id).get_first_time_slots()

    booked_time_slots = Booking.objects.filter(
        resource_fk_id=id,
        date_string=selected_date,
    ).values_list('time_slot', flat=True)

    booked_time_slots_list = [list(slot) for slot in booked_time_slots]

    booked_time_slots_flat = [item for sublist in booked_time_slots_list for item in sublist]

    time_slots_available = sorted(list(set(all_time_slots) - set(booked_time_slots_flat)))
    current_user_name = users.user_name
    user_instance = Users.objects.get(user_name=current_user_name)
    resoruce_instance = Resource.objects.get(resource_id=id)

    if request.method == "POST":
        form = BookingForm(request.POST) 
        if form.is_valid():
            cleaned_data = form.cleaned_data

            cleaned_data['date'] = date

            time_slots = request.POST.getlist('time_slots')

            booking = Booking(
                user=user_instance,
                resource_fk_id=resoruce_instance,
                date=date_type,
                time_slot=time_slots,
                date_string=selected_date,
            )
            booking.save()
            return redirect('check_booking')
        else:
            print(form.errors)
    else:
        form = BookingForm()


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources_booking.html',
        {
            'title':'Booking Resources',
            'id': id,
            'resources': resources,
            'bookings': bookings,
            'year': datetime.now().year,
            'selected_date': selected_date,
            'date_type': date_type, 
            'time_slots_available': time_slots_available,
            'url_date': date,
            'users': users,
            'form': form,
        }
    )

def check_booking(request):
    """Renders the check_booking page."""
    users = get_object_or_404(Users, user=request.user)

    user_bookings = Booking.objects.filter(user=users).order_by('-date')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/check_booking.html',
        {
            'title':'Check Booking',
            'year':datetime.now().year,
            'users': users,
            'user_bookings': user_bookings,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About Us',
            'year':datetime.now().year,
        }
    )

def user_layout(request):
    """Renders the user_layout page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/user_layout.html',
        {
            'title':'User Layout',
            'year':datetime.now().year,
        }
    )

def user_resources(request):
    """Renders the user_resources page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/user_resources.html',
        {
            'title':'Resources',
            'year':datetime.now().year,
        }
    )

@login_required
def bills(request):
    """Renders the bills page."""
    user = request.user
    user_bills = get_object_or_404(Users, user=user)

    for bill in user_bills.bill_set.all():
        for payment in bill.payment_set.all():
            payment.transaction_status = payment.calculate_transaction_status()
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/bills.html',
        {
            'title':'Biils',
            'year':datetime.now().year,
            'users': user,
            'bills': user_bills.bill_set.all(),
        }
    )

@login_required
def make_payment(request, bill_id=None, bill_type=None, total_payment=None):
    """Renders the make_payment page."""
    total_payment = float(total_payment)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            existing_payments = Payment.objects.filter(
                bill_id=bill_id,
                bill_type=bill_type,
                total_payment=total_payment
            )

            if existing_payments.exists():
                payment = existing_payments.first()
                payment.recipient_name = form.cleaned_data['recipient_name']
                payment.payment_amount = form.cleaned_data['payment_amount']
                payment.account_number = form.cleaned_data['account_number']
                payment.card_type = form.cleaned_data['card_type']
                payment.remark = form.cleaned_data['remark']
                payment.payment_date = form.cleaned_data['payment_date']
                payment.transaction_status = payment.calculate_transaction_status()
                if total_payment - payment.payment_amount < 0:
                    error_message = "Total payment cannot be less than zero."
                    return render(
                        request, 
                        'app/make_payment.html', 
                        {
                            'title': 'Make Payment',
                            'year': datetime.now().year,
                            'form': form, 
                            'error_message': error_message
                        })
                else:
                    payment.save()
            else:
                form.save()
            return redirect('bills')
    else:
        initial_data = {
            'bill_id': bill_id,
            'bill_type': bill_type,
            'total_payment': total_payment
        }
        form = PaymentForm(initial=initial_data)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/make_payment.html',
        {
            'title': 'Make Payment',
            'year': datetime.now().year,
            'form': form,
        }
    )

def incident(request):
    """Renders the incident page."""
    incident_reports = IncidentReport.objects.all().order_by('-incident_date')
    search_query = request.GET.get('-incident_date')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/incident.html',
        {
            'title': 'Incident',
            'year': datetime.now().year,
            'incident_reports': incident_reports,
            'search_query':search_query,
        }
    )

def upload_incident(request):
    """Renders the upload_incident page."""
    if request.method == "POST":
        form = IncidentForm(request.POST, request.FILES) 
        if form.is_valid(): 
            incident_report = form.save()
            
            return redirect('incident')

    else:
        form = IncidentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/upload_incident.html',
        {
            'title':'Upload Incident',
            'year':datetime.now().year,
            'form': form
        }
    )

@login_required
def user_details(request):
    """Renders the user_details page."""
    users = get_object_or_404(Users, user=request.user)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/user_details.html',
        {
            'title':'User Details',
            'year':datetime.now().year,
            'users':users,
        }
    )

def edit_user_details(request):
    user_profile = Users.objects.get(user=request.user)
    form = UsersForm(instance=user_profile)
    
    if request.method == 'POST':
        form = UsersForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_details') 

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/edit_user_details.html',
        {
            'title':'Edit User Details',
            'year':datetime.now().year,
            'form': form
        }
    )

def admin_check_booking(request):
    """Renders the check_booking page."""

    user_bookings = Booking.objects.order_by('-date')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_check_booking.html',
        {
            'title':'Admin Check Booking',
            'year':datetime.now().year,
            'user_bookings': user_bookings,
        }
    )

def admin_layout(request):
    """Renders the admin_layout page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_layout.html',
        {
            'title':'Admin Layout',
            'year':datetime.now().year,
        }
    )

def admin_announcement(request):
    """Renders the admin_announcement page."""
    current_time = timezone.now() + timedelta(hours=8)
    announcements = Announcement.objects.all().order_by('-announcement_datetime')
    if request.method == "POST":
        form = AnnouncementForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return redirect('admin_announcement')
    else:
        initial_data = {'announcement_datetime': current_time}
        form = AnnouncementForm(initial=initial_data)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/upload.html',
        {
            'title':'Admin Announcement',
            'year':datetime.now().year,
            'form': form,
            'current_time': current_time,
            'announcements': announcements,
        }
    )

def search_announcements(request):
    all_announcements = Announcement.objects.all().order_by('-announcement_datetime')

    if request.method == "POST":
        searched = request.POST.get('searched')
        if searched:
            filtered_announcements = Announcement.objects.filter(announcement_datetime__contains=searched)
        else:
            filtered_announcements = None

        return render(
            request,
            'app/admin_announcement.html',
            {
                'title':'Searched Announcement',
                'year':datetime.now().year,
                'searched': searched,
                'announcements': all_announcements,
                'filtered_announcements': filtered_announcements,
            }
        )
    else:
        return render(
            request,
            'app/admin_announcement.html',
            {
                'title':'Admin Announcement',
                'year':datetime.now().year,
                'searched': None,
                'announcements': all_announcements,
                'filtered_announcements': None,
            }
        )


def admin_incident(request):
    """Renders the admin_incident page."""
    incident_reports = IncidentReport.objects.all().order_by('-incident_date')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_incident.html',
        {
            'title': 'Admin Incident',
            'year': datetime.now().year,
            'incident_reports': incident_reports,
        }
    )

def admin_payment(request):
    """Renders the admin_payment page."""
    users = request.user 
    bills = Bill.objects.prefetch_related('payment_set').all().order_by('-bill_id')

    for bill in bills:
        for payment in bill.payment_set.all():
            payment.transaction_status = payment.calculate_transaction_status()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_payment.html',
        {
            'title':'Admin Payment',
            'year':datetime.now().year,
            'bills': bills,
            'users':users,
        }
    )

def admin_bills(request):
    """Renders the resources page."""
    if request.method == 'POST':
        form = BillAssignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_payment')
    else:
        form = BillAssignForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_bills.html',
        {
            'title':'Assign Bill',
            'year':datetime.now().year,
            'form': form
        }
    )

def admin_resources(request):
    """Renders the admin_resources page."""
    resources = Resource.objects.all().order_by('resource_id')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_resources.html',
        {
            'title':'Admin resources',
            'year':datetime.now().year,
            'resources': resources,
        }
    )

def admin_add_resources(request):
    """Renders the admin_add_resources page."""
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES) 
        if form.is_valid(): 
            form.save()
            return redirect('admin_resources')
    else:
        form = ResourceForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_add_resources.html',
        {
            'title':'Admin add resources',
            'year':datetime.now().year,
            'form': form,
        }
    )

def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, resource_id=resource_id)
    if request.method == 'POST':
        form = ResourcesForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('admin_resources') 
    else:
        form = ResourcesForm(instance=resource)
    return render(
            request,
            'app/edit_resources.html',
            {
                'title':'Edit resources',
                'year':datetime.now().year,
                'form': form,
            }
        )


def delete_resources(request):
    if request.method == 'POST':
        resource_ids = request.POST.getlist('resource_ids')
        if resource_ids:
            Resource.objects.filter(id__in=resource_ids).delete()
            return redirect('admin_resources')
    return render(
            request,
            'app/admin_resources.html',
            {
                'title':'Delete Resources',
                'year':datetime.now().year,
            }
        )

def admin_user_details(request):
    """Renders the admin_user_details page."""
    users = Users.objects.all().order_by('-user_id')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_user_details.html',
        {
            'title':'Admin User Details',
            'year':datetime.now().year,
            'users':users,
        }
    )

def search_post(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        posts = Users.objects.filter(user_name__icontains=search_query) | Users.objects.filter(room_number__icontains=search_query) | Users.objects.filter(phone_number__icontains=search_query)
        return render(
            request, 
            'app/admin_user_details.html', 
            {
                'title':'Admin User Details',
                'year':datetime.now().year,
                'query': search_query, 
                'users': posts
            }
        )
    else:
        return render(
            request, 
            'app/admin_user_details.html', 
            {
                'title':'Admin User Details',
                'year':datetime.now().year,
            }
        )

def search_ann(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        posts = Announcement.objects.filter(announcement_title__icontains=search_query)
        return render(
            request, 
            'app/admin_announcement.html', 
            {
                'title':'Admin Announcement',
                'year':datetime.now().year,
                'query': search_query, 
                'announcements': posts
            }
        )
    else:
        return render(
            request, 
            'app/admin_announcement.html', 
            {
                'title':'Admin Announcement',
                'year':datetime.now().year,
            }
        )
    
@login_required
def admin_details(request):
    """Renders the admin_details page."""
    admins = get_object_or_404(Admin, admin_name=request.user)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/admin_details.html',
        {
            'title':'User Details',
            'year':datetime.now().year,
            'admins':admins,
        }
    )

def edit_admin_details(request):
    admin_profile = Admin.objects.get(admin_name=request.user)
    form = AdminForm(instance=admin_profile) 
    
    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin_profile)
        if form.is_valid():
            form.save()
            return redirect('admin_details') 

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/edit_admin_details.html',
        {
            'title':'Edit Admin Details',
            'year':datetime.now().year,
            'form': form
        }
    )

@login_required
def menu(request):
    check_user = request.user.groups.filter(name='user').exists()
    check_admin = request.user.groups.filter(name='admin').exists()
    announcements = Announcement.objects.all().order_by('-announcement_datetime')

    context = {
            'title':'Main Menu',
            'is_user': check_user,
            'is_admin': check_admin,
            'year':datetime.now().year,
            'announcements': announcements,
        }
    context['user'] = request.user

    if check_user:
        context.update({'title': 'Menu', 'is_user': True, 'year':datetime.now().year,})
        return render(request, 'app/menu.html', context)
    elif check_admin:
        context.update({'title': 'Admin Menu', 'is_admin': True, 'year':datetime.now().year,})
        return render(request, 'app/admin_menu.html', context)
    else:
        return render(request, 'app/index.html', context)
