# Generated by Django 5.0.3 on 2024-12-21 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0059_rename_tutor_customquestion_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customquestion',
            name='creator',
        ),
        migrations.AddField(
            model_name='customquestion',
            name='tutor',
            field=models.ForeignKey(help_text='The tutor who created this question.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_questions', to='webapp.tutor'),
        ),
    ]