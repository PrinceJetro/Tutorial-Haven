# Generated by Django 5.0.3 on 2024-12-22 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0063_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorialcenter',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
