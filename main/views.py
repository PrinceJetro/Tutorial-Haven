# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import  Student, Course, Department, Topic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import pyttsx3





def home(request):
    return render(request, "cool/index.html")


def register_student(request):
    departments = Department.objects.all()
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name').lower()
        last_name = request.POST.get('last_name').lower()
        department_name = request.POST.get('department')
        phone = request.POST.get('phone')
        email = request.POST.get('email').lower()
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        school = request.POST.get('institution').lower()  # Assuming this is passed as an ID or string
        profile_pic = request.FILES.get('profilepic')  # Retrieve the uploaded image

        # Basic validation
        if username and password and school and first_name and last_name and department_name and phone and email:
            # Fetch the Department instance
            department = get_object_or_404(Department, name=department_name)

            # Create the user and student records
            user = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Create Student instance, including the profile picture
            student = Student(user=user, department=department, phone=phone, school=school, image=profile_pic)
            student.save()
            login(request, user)
            

            return redirect('home')
        else:
            error_message = "All fields are required."

    return render(request, 'register_student.html', {'error_message': error_message, 'alldepartments': departments})

def loginview(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('myprofile')
    return render(request, 'login.html')


@login_required
def list_departments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "cool/departments.html", {"departments": departments})


@login_required
def list_all_courses(request):
    all_courses = Course.objects.all()
    return render(request, 'list_courses.html', {'courses': all_courses})


@login_required
def list_courses(request, department_name=None):
    if department_name:
        department = get_object_or_404(Department, name=department_name)
        print("here")
        courses = department.courses.all()  # Access courses through the related_name
    return render(request, 'list_courses.html', {'courses': courses, "department": department})


@login_required
def course_detail(request, course_name):
    course = get_object_or_404(Course, name=course_name)
    topics = course.topics.all()
    return render(request, 'course_detail.html', {'course': course, 'topics': topics})


@login_required
def topic_detail(request, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)
    return render(request, 'topic_detail.html', {'topic': topic})



@login_required
def myprofile(request):
    user = request.user.username
    courses = Course.objects.all()
    return render(request, 'myprofile.html',{'user': user,'courses': courses} )

