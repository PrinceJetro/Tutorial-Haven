# Generated by Django 5.0.3 on 2024-11-22 11:26

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_grade_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='submission_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for each submission attempt'),
        ),
    ]