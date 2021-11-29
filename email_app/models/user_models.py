from django.db import models
import uuid
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.UUIDField(default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, blank=True)
    gst_details = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
