from django.contrib import admin
from email_app.models.user_models import CompanyProfile, StaffUsers, StaffUsersExcelFile
from email_app.models.subscribers_models import Subscribers, List, Template, Campaigns, GetList, CampaignsLogs, \
    CampaignsLogSubscriber, We360SubscriberReportData


# Register your models here.


class CompanyProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['company_id']
    list_display = ['company_name', 'company_id']


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class StaffAdmin(admin.ModelAdmin):
    list_display = ['unverified_staff_email', 'company_id', 'role_status', 'staff_status']


class StaffUserExcelFileAdmin(admin.ModelAdmin):
    list_display = ['company', 'excel_file_upload', 'isActivated']


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'from_email']


class CampaignLogAdmin(admin.ModelAdmin):
    list_display = ['company', 'campaign', 'log_date', 'email_count', 'is_completed']


class CampaignLogSubscribersAdmin(admin.ModelAdmin):
    list_display = ['campaign_log', 'subscriber_email', 'is_sent']


admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(StaffUsers, StaffAdmin)
admin.site.register(StaffUsersExcelFile, StaffUserExcelFileAdmin)
admin.site.register(List)
admin.site.register(Template)
admin.site.register(GetList)
admin.site.register(Campaigns, CampaignAdmin)
admin.site.register(CampaignsLogs, CampaignLogAdmin)
admin.site.register(CampaignsLogSubscriber, CampaignLogSubscribersAdmin)
admin.site.register(We360SubscriberReportData)
