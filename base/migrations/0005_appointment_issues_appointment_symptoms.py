# Generated by Django 5.1.3 on 2024-11-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_appointment_appointment_id_billing'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='issues',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='symptoms',
            field=models.TextField(null=True),
        ),
    ]
