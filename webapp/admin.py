# admin.py
from django.contrib import admin
from .models import Student, Course, Department, Topic, PastQuestionsObj, KeyPoints, PracticeExplanations, TutorialCenter, Tutor, PastQuestionsTheory, ObjGrade, UserCourseProgress, TheoryGrade, UploadedImage, Achievement, UserAchievement, UserProgress, DiscussionForum, Comment, CustomQuestion, CustomQuestionResponse, ActivityLog


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

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_name', 'percentage', 'attempts')
    list_filter = ('user', 'percentage', 'attempts')

    def course_name(self, obj):
        return obj.course.name  # Adjust this based on the actual field
    course_name.short_description = 'Course'


@admin.register(PastQuestionsObj)
class PastQuestionsObjAdmin(admin.ModelAdmin):
    list_display = ('course', 'question_text', 'uploaded_at')
    search_fields = ('question_text', 'course__name')
    ordering = ('-uploaded_at',)

@admin.register(PastQuestionsTheory)
class PastQuestionsTheoryAdmin(admin.ModelAdmin):
    list_display = ('course', 'year')
    search_fields = ('question_text', 'course__name')
    list_filter = ('course',)
    

@admin.register(ObjGrade)
class ObjGradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'score')
    list_filter = ('course', 'user')
    search_fields = ('user__username', 'course__name', 'question__question_text')
    ordering = ('-submitted_at',)

@admin.register(TheoryGrade)
class TheoryGradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'course', 'score', 'submitted_at')
    list_filter = ('course', 'user')
    search_fields = ('user__username', 'course__name', 'question__question_text')
    ordering = ('-submitted_at',)

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)



@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "required_value", "created_at")
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("created_at",)

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "unlocked_at")
    search_fields = ("user__username", "achievement__name")
    list_filter = ("achievement__category",)
    ordering = ("unlocked_at",)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topics_completed", "courses_completed", "exams_perfect_score", "discussion_posts")
    search_fields = ("user__username",)




@admin.register(DiscussionForum)
class DiscussionForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'creator', 'created_at')
    search_fields = ('title', 'course__title', 'creator__username')
    list_filter = ('course', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('forum', 'commenter', 'content', 'created_at')
    search_fields = ('forum__title', 'commenter__username', 'content')
    list_filter = ('created_at',)





@admin.register(CustomQuestion)
class CustomQuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'tutor', 'created_at')  # Columns to display in the admin list view
    search_fields = ('course__name', 'tutor__name', 'question_text')  # Enable search by these fields
    list_filter = ('course', 'tutor', 'created_at')  # Filters for quick sorting
    ordering = ('-created_at',)  # Order by latest created questions


@admin.register(CustomQuestionResponse)
class CustomQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'student', 'score', 'submitted_at')  # Columns to display
    search_fields = ('question__question_text', 'student__username')  # Searchable fields
    list_filter = ('submitted_at', 'score')  # Filters for quick access
    ordering = ('-submitted_at',)  # Order by latest submissions

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action')
    search_fields = ('user',)