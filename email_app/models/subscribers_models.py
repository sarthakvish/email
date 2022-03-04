from django.db import models
from django.contrib.auth.models import User
from email_app.models.user_models import CompanyProfile
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Subscribers(models.Model):
    class Meta:
        unique_together = (('company', 'email'),)

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
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name


class CampaignsLogs(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    log_date = models.DateTimeField(auto_now_add=True)
    email_count = models.PositiveIntegerField(default=0)
    # STATS_CHOICES = (
    #     ('EMAIL', 'Email'),
    # )
    # messenger = models.CharField(default="EMAIL", choices=MESSENGER_CHOICES, max_length=20)
    is_completed = models.BooleanField(default=False)

    # is_started = models.BooleanField(default=True)
    def __str__(self):
        return str(self.log_date)


class CampaignsLogSubscriber(models.Model):
    campaign_log = models.ForeignKey(CampaignsLogs, on_delete=models.CASCADE)
    subscriber_email = models.CharField(max_length=100)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subscriber_email


class SubscriberEmailData(models.Model):
    subscriber = models.ForeignKey(Subscribers, on_delete=models.CASCADE)
    date = models.DateField()


class GetList(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class We360SubscriberReportData(models.Model):
    subscriber_id = models.PositiveIntegerField()
    subscriber_name = models.CharField(max_length=100)
    mail_to = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=100)
    total_users = models.PositiveIntegerField()
    present_users = models.PositiveIntegerField()
    current_productivity = models.PositiveIntegerField()
    previous_productivity = models.PositiveIntegerField()
    productivity_difference = models.PositiveIntegerField()
    absent_users = models.PositiveIntegerField()
    present_percent = models.PositiveIntegerField()
    absent_percent = models.PositiveIntegerField()
    healthy = models.PositiveIntegerField()
    over_worked = models.PositiveIntegerField()
    under_utilised = models.PositiveIntegerField()
    working_time = models.PositiveIntegerField()
    active_time = models.PositiveIntegerField()
    idle_time = models.PositiveIntegerField()
    break_time = models.PositiveIntegerField()
    attendence_csv_url = models.CharField(max_length=255)

    def __str__(self):
        return self.subscriber_name
