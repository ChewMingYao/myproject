# Generated by Django 4.1.4 on 2024-02-06 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_admin_announcement_bill_incidentreport_resource_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='booking_date',
        ),
    ]
