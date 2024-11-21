# Generated by Django 5.0.3 on 2024-11-21 23:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_remove_institution_owner_institution_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='school',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(null=True, upload_to='uploaded_image'),
        ),
        migrations.CreateModel(
            name='TutorialCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('image', models.ImageField(null=True, upload_to='uploaded_image')),
                ('phone', models.IntegerField(null=True)),
                ('discipline', models.CharField(max_length=200, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tutorial_center', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='uploaded_image')),
                ('is_approved', models.BooleanField(default=False)),
                ('phone', models.IntegerField(null=True)),
                ('speciality', models.ManyToManyField(null=True, related_name='tutors', to='webapp.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tutorial_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutors', to='webapp.tutorialcenter')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tutorial_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='webapp.tutorialcenter'),
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
