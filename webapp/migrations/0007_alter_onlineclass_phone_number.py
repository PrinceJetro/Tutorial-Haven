# Generated by Django 5.0.3 on 2024-05-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_rename_phone_numbber_onlineclass_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineclass',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
