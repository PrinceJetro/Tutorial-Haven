# Generated by Django 5.0.3 on 2024-12-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0056_alter_student_user_alter_tutor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customquestionresponse',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Score for the response, out of 100.', max_digits=5, null=True),
        ),
    ]
