# Generated by Django 5.0.3 on 2024-11-22 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_alter_practiceexplanations_cbt_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='webapp.course'),
        ),
    ]
