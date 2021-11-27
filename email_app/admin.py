from django.contrib import admin
from email_app.models.user_models import CompanyProfile

# Register your models here.


class CompanyProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['company_id']
    list_display = ['company_name', 'company_id']


admin.site.register(CompanyProfile, CompanyProfileAdmin)
