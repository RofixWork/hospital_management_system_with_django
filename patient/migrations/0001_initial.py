# Generated by Django 5.1.3 on 2024-11-18 16:46

import django.db.models.deletion
import utils.custom_validations
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=40, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[utils.custom_validations.CustomValidations.check_phone_number])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('type', models.CharField(blank=True, choices=[('scheduled appointment', 'Scheduled Appointment'), ('cancelled appointment', 'Cancelled Appointment')], max_length=30, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.patient')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]