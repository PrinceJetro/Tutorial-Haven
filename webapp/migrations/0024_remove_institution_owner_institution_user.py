# Generated by Django 5.0.3 on 2024-11-20 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_student_is_approved'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='owner',
        ),
        migrations.AddField(
            model_name='institution',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_schools', to=settings.AUTH_USER_MODEL),
        ),
    ]
