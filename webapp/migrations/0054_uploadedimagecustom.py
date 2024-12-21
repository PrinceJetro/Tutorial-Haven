# Generated by Django 5.0.3 on 2024-12-21 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0053_customquestion_customquestionresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImageCustom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=5000, null=True, upload_to='uploaded_images')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('custom_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='webapp.customquestionresponse')),
            ],
        ),
    ]
