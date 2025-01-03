# Generated by Django 5.0.3 on 2024-11-22 08:32

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_remove_student_phone_remove_tutor_phone_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='practiceexplanations',
            name='cbt_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='explanations', to='webapp.pastquestions'),
        ),
        migrations.RemoveField(
            model_name='pastquestions',
            name='content',
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='correct_option',
            field=models.CharField(blank=True, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], help_text='Correct option for CBT questions (leave blank for theory)', max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='option_a',
            field=models.CharField(blank=True, help_text='Option A for CBT questions (leave blank for theory)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='option_b',
            field=models.CharField(blank=True, help_text='Option B for CBT questions (leave blank for theory)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='option_c',
            field=models.CharField(blank=True, help_text='Option C for CBT questions (leave blank for theory)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='option_d',
            field=models.CharField(blank=True, help_text='Option D for CBT questions (leave blank for theory)', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='question_text',
            field=ckeditor.fields.RichTextField(help_text='Question for the CBT or theory question', null=True),
        ),
        migrations.AddField(
            model_name='pastquestions',
            name='theory',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Detailed theory content if applicable'),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_theory', models.BooleanField(default=False, help_text='Indicates if the question was theory or CBT')),
                ('score', models.DecimalField(decimal_places=2, help_text='Score for this question', max_digits=5)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='webapp.pastquestions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TheorySubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', ckeditor.fields.RichTextField(help_text="User's answer to the theory question")),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('graded', models.BooleanField(default=False, help_text='Has this submission been graded?')),
                ('grade', models.DecimalField(blank=True, decimal_places=2, help_text='Grade for this submission', max_digits=5, null=True)),
                ('feedback', ckeditor.fields.RichTextField(blank=True, help_text='Optional feedback for the user')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theory_submissions', to='webapp.pastquestions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theory_submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CBTQuestion',
        ),
    ]
