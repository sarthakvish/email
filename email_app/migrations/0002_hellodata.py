# Generated by Django 3.2.9 on 2022-03-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hellodata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_name', models.CharField(max_length=100)),
                ('mail_to', models.CharField(max_length=255)),
            ],
        ),
    ]