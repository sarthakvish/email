from django.db import models
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Subscribers(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=True)
    SUBSCRIBERS_CHOICES = (
        ('ENABLED', 'Enabled'),
        ('BLACKLISTED', 'Blacklisted'),
    )
    subscriber_status = models.CharField(default="ENABLED", choices=SUBSCRIBERS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class List(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    subscriber = models.ManyToManyField(Subscribers)
    name = models.CharField(max_length=100)
    LISTS_CHOICES = (
        ('PRIVATE', 'Private'),
        ('PUBLIC', 'Public'),
    )
    list_type = models.CharField(default="ENABLED", choices=LISTS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    tags = TaggableManager()


class Template(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)