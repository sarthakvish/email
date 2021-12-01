from django.db import models
import uuid
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_id")
    company_id = models.UUIDField(default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, blank=True)
    gst_details = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class StaffUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    unverified_staff_email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    ADMINISTRATOR = 0
    CAMPAIGN_MANAGER = 1
    VIEWER = 2
    ROLLS_CHOICES = (
        (ADMINISTRATOR, 'administrator'),
        (CAMPAIGN_MANAGER, 'campaign_manager'),
    )
    role_status = models.IntegerField(default=2, choices=ROLLS_CHOICES)

    PENDING = 0
    INVITED = 1
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (INVITED, 'Invited'),
    )
    staff_status = models.IntegerField(default=0, choices=STATUS_CHOICES)
