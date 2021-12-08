# Generated by Django 3.2.9 on 2021-12-08 06:51

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('is_gst_registered', models.BooleanField(default=False)),
                ('gst_details', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', ckeditor.fields.RichTextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('subscriber_status', models.CharField(choices=[('ENABLED', 'Enabled'), ('BLACKLISTED', 'Blacklisted')], default='ENABLED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffUsersExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file_upload', models.FileField(upload_to='excel')),
                ('isActivated', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unverified_staff_email', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role_status', models.CharField(choices=[('ADMINISTRATOR', 'administrator'), ('CAMPAIGN_MANAGER', 'campaign_manager')], default='CAMPAIGN_MANAGER', max_length=20)),
                ('staff_status', models.CharField(choices=[('PENDING', 'Pending'), ('INVITED', 'Invited'), ('VERIFIED', 'Verified')], default='INVITED', max_length=15)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('list_type', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], default='ENABLED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile')),
                ('subscriber', models.ManyToManyField(to='email_app.Subscribers')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
