# Generated by Django 3.2.9 on 2022-02-11 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0017_alter_campaignslogsubscriber_campaign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignslogsubscriber',
            name='campaign',
        ),
        migrations.AddField(
            model_name='campaignslogsubscriber',
            name='campaign_log',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='email_app.campaignslogs'),
            preserve_default=False,
        ),
    ]
