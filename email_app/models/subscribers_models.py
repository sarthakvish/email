from django.db import models
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
