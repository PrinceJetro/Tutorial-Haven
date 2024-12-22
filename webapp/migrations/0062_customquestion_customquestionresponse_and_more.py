# Generated by Django 5.0.3 on 2024-12-21 23:47

import ckeditor.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0061_remove_customquestionresponse_question_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', ckeditor.fields.RichTextField(help_text='Enter the theory question in rich text format.')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time the question was created.')),
                ('course', models.ForeignKey(help_text='The course this question belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='custom_questions', to='webapp.course')),
                ('tutor', models.ForeignKey(help_text='The tutor who created this question.', on_delete=django.db.models.deletion.CASCADE, related_name='custom_questions', to='webapp.tutor')),
            ],
        ),
        migrations.CreateModel(
            name='CustomQuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', ckeditor.fields.RichTextField(help_text="Student's answer to the question.")),
                ('score', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Score for the response, out of 100.', max_digits=5, null=True)),
                ('note', ckeditor.fields.RichTextField(blank=True, help_text='Feedback or note for the student from the tutor.', null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True, help_text='The date and time the response was submitted.')),
                ('submission_id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID for the submission.', unique=True)),
                ('question', models.ForeignKey(help_text='The question being answered.', on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='webapp.customquestion')),
                ('student', models.ForeignKey(help_text='The student who submitted the response.', on_delete=django.db.models.deletion.CASCADE, related_name='custom_responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
