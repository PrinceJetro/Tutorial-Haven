# Generated by Django 5.0.3 on 2024-12-07 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0041_remove_tutor_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
