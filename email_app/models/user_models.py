from django.core.validators import RegexValidator
from django.db import models
import uuid
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.UUIDField(default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    is_gst_registered = models.BooleanField(default=False)
    gst_details = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class StaffUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    unverified_staff_email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    ROLLS_CHOICES = (
        ('ADMINISTRATOR', 'administrator'),
        ('CAMPAIGN_MANAGER', 'campaign_manager'),
    )
    role_status = models.CharField(default="CAMPAIGN_MANAGER", choices=ROLLS_CHOICES, max_length=20)

    STATUS_CHOICES = (
        ('PENDING', 'Pending',),
        ('INVITED', 'Invited',),
        ('VERIFIED', 'Verified',),
    )
    staff_status = models.CharField(default="INVITED", choices=STATUS_CHOICES,  max_length=15)


class StaffUsersExcelFile(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    excel_file_upload = models.FileField(upload_to="excel")
    isActivated = models.BooleanField(default=False)
