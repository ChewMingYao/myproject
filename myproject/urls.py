"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from app import views, forms
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.sign_up, name="sign_up"),
    re_path(r'^accounts/login/$',
        LoginView.as_view(template_name = 'app/menu.html'),
        name='menu'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^resources_entertainment$', views.resources_entertainment, name='resources_entertainment'),
    re_path(r'^resources_learning$', views.resources_learning, name='resources_learning'),
    re_path(r'^resources_sports$', views.resources_sports, name='resources_sports'),
    path('resources_booking/<str:id>/<str:date>/', views.resources_booking, name='resources_booking'),
    re_path(r'^check_booking$', views.check_booking, name='check_booking'),
    re_path(r'^admin_check_booking$', views.admin_check_booking, name='admin_check_booking'),
    re_path(r'^about$', views.about, name='about'),
    re_path(r'^login/$',
        LoginView.as_view(template_name = 'app/login.html'),
        name='login'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^sign_up$', views.sign_up, name='sign_up'),
    re_path(r'^menu$', views.menu, name='menu'),
    re_path(r'^user_layout$', views.user_layout, name='user_layout'),
    re_path(r'^user_resources$', views.user_resources, name='user_resources'),
    re_path(r'^bills$', views.bills, name='bills'),
    re_path(r'^make_payment/(?P<bill_id>[\w#]+)/(?P<bill_type>[^/]+)/(?P<total_payment>[^/]+)/$', views.make_payment, name='make_payment'),
    re_path(r'^incident$', views.incident, name='incident'),
    re_path(r'^upload_incident$', views.upload_incident, name='upload_incident'),
    re_path(r'^user_details$', views.user_details, name='user_details'),
    re_path(r'^edit_user_details$', views.edit_user_details, name='edit_user_details'),
    
    re_path(r'^admin_layout$', views.admin_layout, name='admin_layout'),
    re_path(r'^admin_announcement$', views.search_announcements, name='admin_announcement'),
    re_path(r'^search_announcements$', views.search_announcements, name='search_announcements'),
    re_path(r'^admin_incident$', views.admin_incident, name='admin_incident'),
    re_path(r'^admin_payment$', views.admin_payment, name='admin_payment'),
    re_path(r'^admin_bills$', views.admin_bills, name='admin_bills'),
    re_path(r'^admin_resources$', views.admin_resources, name='admin_resources'),
    re_path(r'^admin_add_resources$', views.admin_add_resources, name='admin_add_resources'),
    re_path(r'^admin_user_details$', views.admin_user_details, name='admin_user_details'),
    path('search/', views.search_post, name='search-post'),
    path('search/ann', views.search_ann, name='search-ann'),
    re_path(r'^admin_details$', views.admin_details, name='admin_details'),
    re_path(r'^edit_admin_details$', views.edit_admin_details, name='edit_admin_details'),
    re_path(r'^upload$', views.admin_announcement, name="upload"),
    path('edit_resources/<str:resource_id>/', views.edit_resource, name='edit_resource'),
    path('delete_resources/', views.delete_resources, name='delete_resources'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
