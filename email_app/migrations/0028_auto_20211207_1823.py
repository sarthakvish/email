# Generated by Django 3.2.9 on 2021-12-07 12:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0027_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='name',
        ),
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
