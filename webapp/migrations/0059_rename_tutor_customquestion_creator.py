# Generated by Django 5.0.3 on 2024-12-21 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0058_alter_customquestion_tutor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customquestion',
            old_name='tutor',
            new_name='creator',
        ),
    ]
