from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Institution(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_schools", null=True)
    image = models.ImageField(upload_to="uploaded_image", null=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)


    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_image", null=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    school = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='teachers')
    is_approved = models.BooleanField(default=False)  # Approval field

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    departments = models.ManyToManyField(Department, related_name='courses')  # ManyToManyField
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage score


    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploaded_image", null=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    school = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, related_name='students')  # Foreign key to Institution
    is_approved = models.BooleanField(default=False)  # Approval field

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Topic(models.Model):
    name = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.name


class PastQuestions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='past_questions')
    content = RichTextField(blank=True)
    year = models.CharField(max_length=4, help_text="Year of the examination")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.name} Past Questions ({self.year})'


class KeyPoints(models.Model):
    past_question = models.ForeignKey(PastQuestions, on_delete=models.CASCADE, related_name='key_points')
    content = RichTextField(help_text="Key points or brief answers related to past questions", blank=True)
    
    def __str__(self):
        return f'Key Points for {self.past_question.course.name} ({self.past_question.year})'


class CBTQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cbt_questions')
    question_text = RichTextField(help_text="Question for the CBT")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])

    def __str__(self):
        return f'CBT Question for {self.course.name}'


class PracticeExplanations(models.Model):
    cbt_question = models.ForeignKey(CBTQuestion, on_delete=models.CASCADE, related_name='explanations')
    explanation = RichTextField(help_text="Explanation for the correct answer in CBT")

    def __str__(self):
        return f'Explanation for {self.cbt_question.course.name} CBT Question'
