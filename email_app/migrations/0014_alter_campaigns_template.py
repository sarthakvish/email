# Generated by Django 3.2.9 on 2022-01-24 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0013_auto_20220119_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigns',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='email_app.template'),
        ),
    ]