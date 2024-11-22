# admin.py
from django.contrib import admin
from .models import Student, Course, Department, Topic, PastQuestions, KeyPoints, PracticeExplanations, TutorialCenter, Tutor, TheorySubmission, Grade, UserCourseProgress



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TutorialCenter)
class TutorialCenterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_departments')  # Use custom method for departments
    search_fields = ('name', 'departments__name')
    list_filter = ('departments',)  # Filter by the `departments` field

    def get_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])  # Display departments as a comma-separated list

    get_departments.short_description = 'Departments'  # Set column name for departments

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    search_fields = ('name', 'course__name')
    list_filter = ('course',)


@admin.register(PastQuestions)
class PastQuestionsAdmin(admin.ModelAdmin):
    list_display = ('course', 'year', 'question_text')
    search_fields = ('course__name', 'year')
    list_filter = ('course', 'year')
    ordering = ('-uploaded_at',)

@admin.register(KeyPoints)
class KeyPointsAdmin(admin.ModelAdmin):
    list_display = ('past_question', 'content')
    search_fields = ('past_question__course__name', 'past_question__year')
    list_filter = ('past_question__course',)


@admin.register(PracticeExplanations)
class PracticeExplanationsAdmin(admin.ModelAdmin):
    list_display = ('cbt_question', 'explanation')
    search_fields = ('cbt_question__course__name', 'cbt_question__question_text')
    list_filter = ('cbt_question__course',)


@admin.register(TheorySubmission)
class TheorySubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'submitted_at')
    list_filter = ('user', 'submitted_at')
    search_fields = ('user__username', 'question__question_text')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'score', )
    list_filter = ('user', 'question',)

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_name', 'percentage', 'attempts')
    list_filter = ('user', 'percentage', 'attempts')

    def course_name(self, obj):
        return obj.course.name  # Adjust this based on the actual field
    course_name.short_description = 'Course'
