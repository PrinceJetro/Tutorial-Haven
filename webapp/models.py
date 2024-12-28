from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid  # To generate unique submission IDs
from django.utils.timezone import now



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
    image = models.ImageField(upload_to="uploaded_image", null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    is_active = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.name


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tutor")
    image = models.ImageField(upload_to="uploaded_image", null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='tutors')
    is_approved = models.BooleanField(default=False)  # Approval field
    speciality = models.ManyToManyField(Course, related_name='speciality', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="student")
    image = models.ImageField(upload_to="uploaded_image", null=True,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKKOdmJz8Z2pDtYgFgR2u9spABvNNPKYYtGw&s', max_length=5000)
    tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='students', null=True)
    is_approved = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')  # Foreign key to Department
    

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Topic(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True)
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
    question_text = models.TextField(help_text="Theory question")
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


class UploadedImage(models.Model):
    theory_grade = models.ForeignKey(TheoryGrade, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="uploaded_images", max_length=5000, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Submission {self.theory_grade.submission_id}"

        
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


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('engagement', 'Engagement'),
        ('performance', 'Performance'),
        ('milestone', 'Milestone'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    badge = models.ImageField(upload_to="achievement_badges", null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    required_value = models.IntegerField(default=0, help_text="Value to meet criteria (e.g., 5 courses, 7 days, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="user_achievements")
    unlocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class UserProgress(models.Model):
    """Tracks user progress to evaluate achievements."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progress")
    topics_completed = models.IntegerField(default=0)  # Optional but useful for caching
    completed_topics = models.ManyToManyField("Topic", blank=True, related_name="users_completed")
    courses_completed = models.IntegerField(default=0)
    exams_perfect_score = models.IntegerField(default=0)
    discussion_posts = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress for {self.user.username}"



class DiscussionForum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="forums", null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forums")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    forum = models.ForeignKey(DiscussionForum, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.forum.title}"

class CustomQuestion(models.Model):
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='custom_questions',
        help_text="The course this question belongs to."
    )
    question_text = RichTextField(help_text="Enter the theory question in rich text format.")
    tutor = models.ForeignKey(
        'Tutor', on_delete=models.CASCADE, related_name='custom_questions',
        help_text="The tutor who created this question."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the question was created.")

    def __str__(self):
        return f'{self.course.name} - {self.tutor.user.username}\'s Question posted {self.created_at}'


class CustomQuestionResponse(models.Model):
    question = models.ForeignKey(
        CustomQuestion, on_delete=models.CASCADE, related_name='responses',
        help_text="The question being answered."
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='custom_responses',
        help_text="The student who submitted the response."
    )
    response = RichTextField(help_text="Student's answer to the question.")
    score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, default=0,
        help_text="Score for the response, out of 100."
    )
    note = RichTextField(
        null=True, blank=True, help_text="Feedback or note for the student from the tutor."
    )
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the response was submitted.")
    submission_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, help_text="Unique ID for the submission."
    )

    def __str__(self):
        return f'{self.student.username} - {self.question.course.name} Response'


class UploadedImageCustom(models.Model):
    custom_grade = models.ForeignKey(CustomQuestionResponse, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="uploaded_images", max_length=5000, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Submission {self.theory_grade.submission_id}"



class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255, help_text="Description of the action performed")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"



# class CustomTopic(models.Model):
#     name = models.CharField(max_length=255)
#     content = models.TextField(blank=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')

#     def __str__(self):
#         return self.name




# class Feedback(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
#     tutorial_center = models.ForeignKey(TutorialCenter, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
#     rating = models.PositiveIntegerField(default=0, help_text="Rating out of 5")
#     comments = models.TextField(help_text="Feedback comments", blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback by {self.user.username} - {self.rating}/5"
