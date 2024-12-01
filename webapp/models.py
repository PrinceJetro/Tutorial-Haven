from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid  # To generate unique submission IDs


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, null=True)
    departments = models.ManyToManyField(Department, related_name='courses')  # ManyToManyField


    def __str__(self):
        return self.name

class TutorialCenter(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutorial_center')
    image = models.ImageField(upload_to="uploaded_image", null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s')
    def __str__(self):
        return self.name


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_image", null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s')
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='tutors')
    is_approved = models.BooleanField(default=False)  # Approval field
    speciality = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='speciality', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_image", null=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='students', null=True)
    is_approved = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')  # Foreign key to Department
    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Topic(models.Model):
    name = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.name



class PastQuestionsObj(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objective_questions')
    question_text = RichTextField(help_text="CBT question")
    option_a = models.CharField(max_length=200, blank=True, null=True, help_text="Option A (leave blank for theory)")
    option_b = models.CharField(max_length=200, blank=True, null=True, help_text="Option B (leave blank for theory)")
    option_c = models.CharField(max_length=200, blank=True, null=True, help_text="Option C (leave blank for theory)")
    option_d = models.CharField(max_length=200, blank=True, null=True, help_text="Option D (leave blank for theory)")
    correct_option = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        help_text="Correct option (leave blank for theory)"
    )
    year = models.CharField(max_length=4, help_text="Year of the examination", null=True)
    body = models.CharField(max_length=4, help_text="Waec / Jamb?", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.name} CBT Question: {self.question_text[:50]}'

class ObjGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objective_grades')
    question = models.ForeignKey(PastQuestionsObj, on_delete=models.CASCADE, related_name='obj_grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='objective_grades', null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, help_text="Score")
    submitted_at = models.DateTimeField(auto_now_add=True)
    submission_id = models.UUIDField(default=uuid.uuid4, editable=False, help_text="Unique submission ID")

    def __str__(self):
        return f'{self.user.username} - {self.course.name} Objective Grade'

class PastQuestionsTheory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='theory_questions')
    question_text = RichTextField(help_text="Theory question")
    year = models.CharField(max_length=4, help_text="Year of the examination", null=True)

    def __str__(self):
        return f'{self.course.name} Theory Question: {self.year}'

class TheoryGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theory_grades')
    question = models.ForeignKey(PastQuestionsTheory, on_delete=models.CASCADE, related_name='theory_grades')
    question_text = RichTextField(help_text="Theory question", null=True)
    response = RichTextField(help_text="Student's response", null=True)
    note = RichTextField(help_text="Note for Student", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='theory_grades', null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Score Over 100", null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submission_id = models.UUIDField(default=uuid.uuid4, editable=False, help_text="Unique submission ID")

    def __str__(self):
        return f'{self.user.username} - {self.course.name} Theory Grade {self.question.year}'


class UserCourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="User's progress percentage for the course")
    attempts = models.PositiveIntegerField(default=0, help_text="Number of attempts by the user for this course")

    def __str__(self):
        return f"{self.user.username} - {self.course.name}: {self.percentage}% in {self.course}"




class KeyPoints(models.Model):
    past_question = models.ForeignKey(PastQuestionsObj, on_delete=models.CASCADE, related_name='key_points')
    content = RichTextField(help_text="Key points or brief answers related to past questions", blank=True)
    
    def __str__(self):
        return f'Key Points for {self.past_question.course.name} ({self.past_question.year})'



class PracticeExplanations(models.Model):
    cbt_question = models.ForeignKey(PastQuestionsObj, on_delete=models.CASCADE, related_name='explanations')
    explanation = RichTextField(help_text="Explanation for the correct answer in CBT")

    def __str__(self):
        return f'Explanation for {self.cbt_question.course.name} CBT Question'