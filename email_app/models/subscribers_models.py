from django.db import models
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Subscribers(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, blank=True)
    SUBSCRIBERS_CHOICES = (
        ('ENABLED', 'Enabled'),
        ('BLACKLISTED', 'Blacklisted'),
    )
    is_active = models.BooleanField(default=True)
    subscriber_status = models.CharField(default="ENABLED", choices=SUBSCRIBERS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class List(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    subscriber = models.ManyToManyField(Subscribers)
    name = models.CharField(max_length=100, unique=True)
    LISTS_CHOICES = (
        ('PRIVATE', 'Private'),
        ('PUBLIC', 'Public'),
    )
    list_type = models.CharField(default="PUBLIC", choices=LISTS_CHOICES, max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name


class Template(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = RichTextUploadingField()
    discription = models.TextField(default="hello")
    template = models.FileField(upload_to="email")
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


class Campaigns(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    from_email = models.CharField(max_length=255)
    MESSENGER_CHOICES = (
        ('EMAIL', 'Email'),
    )
    list = models.ManyToManyField(List)
    messenger = models.CharField(default="EMAIL", choices=MESSENGER_CHOICES, max_length=20)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name
