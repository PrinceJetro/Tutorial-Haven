# admin.py
from django.contrib import admin
from .models import Student, Course, Department, Topic

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'tutorial_center__name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
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
