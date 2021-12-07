# Generated by Django 3.2.9 on 2021-12-07 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0022_auto_20211207_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribers',
            name='user',
        ),
        migrations.AddField(
            model_name='subscribers',
            name='company',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='email_app.companyprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscribers',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='subscribers',
            name='subscriber_status',
            field=models.CharField(choices=[('ENABLED', 'Enabled'), ('BLACKLISTED', 'Blacklisted')], default='ENABLED', max_length=20),
        ),
        migrations.AddField(
            model_name='subscribers',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]