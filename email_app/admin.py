from django.contrib import admin
from email_app.models.user_models import CompanyProfile, StaffUsers
from email_app.models.subscribers_models import Subscribers


# Register your models here.


class CompanyProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['company_id']
    list_display = ['company_name', 'company_id']


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class StaffAdmin(admin.ModelAdmin):
    list_display = ['unverified_staff_email', 'company_id', 'role_status']


admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(StaffUsers, StaffAdmin)
