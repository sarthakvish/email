# Generated by Django 3.2.9 on 2021-12-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0015_alter_staffusers_staff_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffusers',
            name='staff_status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Invited'), (2, 'Verified')], default=1),
        ),
    ]
