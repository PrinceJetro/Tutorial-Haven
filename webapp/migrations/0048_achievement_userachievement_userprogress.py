# Generated by Django 5.0.3 on 2024-12-18 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0047_remove_theorygrade_image_uploadedimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('badge', models.ImageField(blank=True, null=True, upload_to='achievement_badges')),
                ('category', models.CharField(choices=[('engagement', 'Engagement'), ('performance', 'Performance'), ('milestone', 'Milestone')], max_length=50)),
                ('required_value', models.IntegerField(default=0, help_text='Value to meet criteria (e.g., 5 courses, 7 days, etc.)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unlocked_at', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='webapp.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics_completed', models.IntegerField(default=0)),
                ('courses_completed', models.IntegerField(default=0)),
                ('exams_perfect_score', models.IntegerField(default=0)),
                ('discussion_posts', models.IntegerField(default=0)),
                ('login_streak', models.IntegerField(default=0)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
