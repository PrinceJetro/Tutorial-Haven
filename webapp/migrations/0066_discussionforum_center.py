# Generated by Django 5.0.3 on 2025-01-02 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0065_customquestion_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionforum',
            name='center',
            field=models.CharField(blank=True, null=True),
        ),
    ]
