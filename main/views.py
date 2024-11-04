# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import OwnerRegistrationForm, TutorRegistrationForm, StudentRegistrationForm, CourseForm
from .models import TutorialCenter, Tutor, Student, Course, Exam, Department, Topic
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


def register_owner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tutorial_center_name = request.POST.get('tutorial_center_name')
        tutorial_center_address = request.POST.get('tutorial_center_address')
        tutorial_center_number = request.POST.get('tutorial_center_number')
        tutorial_center_discipline = request.POST.get('tutorial_center_discipline')

        # Basic validation
        if username and password and tutorial_center_name:
            user = User(username=username, password=make_password(password))
            user.save()
            
            tutorial_center = TutorialCenter(name=tutorial_center_name, owner=user, address=tutorial_center_address, discipline=tutorial_center_discipline, phone=tutorial_center_number)
            tutorial_center.save()

            return redirect('home')
        else:
            error_message = "All fields are required."

    return render(request, 'register_owner.html', {'error_message': error_message if 'error_message' in locals() else ''})

def register_tutor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tutorial_center_id = request.POST.get('tutorial_center')  # Assuming the tutorial center is passed as an ID

        # Basic validation
        if username and password and tutorial_center_id:
            user = User(username=username, password=make_password(password))
            user.save()

            tutor = Tutor(user=user, tutorial_center_id=tutorial_center_id, is_approved=False)
            tutor.save()

            return redirect('home')
        else:
            error_message = "All fields are required."

    return render(request, 'register_tutor.html', {'error_message': error_message if 'error_message' in locals() else ''})

def register_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tutorial_center_id = request.POST.get('tutorial_center')  # Assuming the tutorial center is passed as an ID

        # Basic validation
        if username and password and tutorial_center_id:
            user = User(username=username, password=make_password(password))
            user.save()

            student = Student(user=user, tutorial_center_id=tutorial_center_id, is_approved=False)
            student.save()

            return redirect('home')
        else:
            error_message = "All fields are required."

    return render(request, 'register_student.html', {'error_message': error_message if 'error_message' in locals() else ''})

def loginview(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        print("Hereeee")
        if user:
            login(request, user)
            return redirect('myprofile')
    return render(request, 'login.html')

@login_required
def approve_users(request):
    tutorial_center = get_object_or_404(TutorialCenter, owner=request.user)
    unapproved_tutors = Tutor.objects.filter(tutorial_center=tutorial_center, is_approved=False)
    unapproved_students = Student.objects.filter(tutorial_center=tutorial_center, is_approved=False)

    if request.method == 'POST':
        # Process approvals for selected tutors and students
        approved_tutor_ids = request.POST.getlist('approve_tutors')
        approved_student_ids = request.POST.getlist('approve_students')

        Tutor.objects.filter(id__in=approved_tutor_ids).update(is_approved=True)
        Student.objects.filter(id__in=approved_student_ids).update(is_approved=True)

        return redirect('approve_users')

    return render(request, 'approve_users.html', {
        'unapproved_tutors': unapproved_tutors,
        'unapproved_students': unapproved_students,
    })



@login_required
def list_departments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "cool/departments.html", {"departments": departments})


@login_required
def create_course(request):
    if request.method == "POST":
        # Assume you have a CourseForm that includes department selection
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to list or detail view
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

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
def about_tutorial(request):
    pass



@login_required
def list_tutorial_students(request, tutorial):
    # Get the tutorial center by name or return 404 if not found
    center = get_object_or_404(TutorialCenter, name=tutorial)
    
    # Check if the user is the owner or an approved tutor associated with the center
    if request.user != center.owner and not Tutor.objects.filter(user=request.user, tutorial_center=center, is_approved=True).exists():
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Get only approved students associated with the center
    students = center.students.filter(is_approved=True)

    return render(request, 'tutorial_students.html', {'students': students, 'center': center})


@login_required
def myprofile(request):
    user = request.user.username
    courses = Course.objects.all()
    return render(request, 'myprofile.html',{'user': user,'courses': courses} )

    

@login_required
def speech(request, texts):
    # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set the text you want to convert to speech
        text = texts

        # Use the engine to say the text
        engine.say(text)

        # Wait for the speaking to finish
        engine.runAndWait()

