# Generated by Django 5.1.3 on 2024-11-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='doctors_available',
            field=models.PositiveIntegerField(null=True),
        ),
    ]