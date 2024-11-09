# Generated by Django 5.0.3 on 2024-11-08 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_institution_cbtquestion_percentage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cbtquestion',
            name='percentage',
        ),
        migrations.AddField(
            model_name='course',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
