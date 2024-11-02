# models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField



class TutorialCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutorial_center')
    phone = models.IntegerField(max_length=11, null=True)
    discipline = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='tutors')
    is_approved = models.BooleanField(default=False)  # Approval field

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='students')
    is_approved = models.BooleanField(default=False)  # Approval field

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Department(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    departments = models.ManyToManyField(Department, related_name='courses')  # Updated to ManyToManyField


    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = RichTextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.name
    


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    duration = models.DurationField()  # Duration of the exam
    maximum_marks = models.PositiveIntegerField()

    def __str__(self):
        return f'Exam for {self.course.title} on {self.date}'
    