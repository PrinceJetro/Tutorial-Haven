# Generated by Django 5.0.3 on 2024-12-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0044_alter_tutor_image_alter_tutorialcenter_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastquestionstheory',
            name='question_text',
            field=models.TextField(help_text='Theory question'),
        ),
    ]
