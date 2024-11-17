# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import  Student, Course, Department, Topic,CBTQuestion, Institution, PastQuestions, KeyPoints, Institution, Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from webapp.storage import SupabaseStorage





def home(request):
    return render(request, "cool/index.html")



def register_institution(request):
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name').lower()
        last_name = request.POST.get('last_name').lower()
        email = request.POST.get('email').lower()
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        school_name = request.POST.get('school_name')
        profile_pic = request.FILES.get('profilepic')  # Retrieve the uploaded image


        # Initialize storage
        storage = SupabaseStorage()

        # Handle image upload
        image_url = None
        if profile_pic:
            post = 'media/' + profile_pic.name
            print(profile_pic.name)
            try:
                filename = storage.save(post, profile_pic)
                image_url = storage.url(filename)
            except Exception as e:
                error_message = "Failed to upload image to Supabase storage. Please try again."
                print(f"Error uploading image: {e}")

        # Basic validation
        if username and password  and first_name and last_name  and email and school_name:

            # Create the user and student records
            user = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Create Student instance, including the profile picture if uploaded
            institution = Institution(
                owner=user,
                name= school_name,
                image=image_url  # Store the image URL instead of the file
            )
            institution.save()
            login(request, user)

            return redirect('myprofile')
        else:
            error_message = "All fields are required."

    return render(request, 'register_institution.html', {'error_message': error_message})




def register_teacher(request):
    allinstitutions = Institution.objects.all()
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name').lower()
        last_name = request.POST.get('last_name').lower()
        email = request.POST.get('email').lower()
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        school = request.POST.get('institution').lower()  # Assuming this is passed as an ID or string
        profile_pic = request.FILES.get('profilepic')  # Retrieve the uploaded image
        print("profile_pic.name")


        # Initialize storage
        storage = SupabaseStorage()

        # Handle image upload
        image_url = None
        if profile_pic:
            post = 'media/' + profile_pic.name
            print(profile_pic.name)
            try:
                filename = storage.save(post, profile_pic)
                image_url = storage.url(filename)
            except Exception as e:
                error_message = "Failed to upload image to Supabase storage. Please try again."
                print(f"Error uploading image: {e}")

        # Basic validation
        if username and password and school and first_name and last_name and email:

            # Create the user and student records
            user = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Create Student instance, including the profile picture if uploaded
            teacher = Teacher(
                user=user,
                school=school,
                image=image_url  # Store the image URL instead of the file
            )
            teacher.save()
            login(request, user)

            return redirect('myprofile')
        else:
            error_message = "All fields are required."
    return render(request, 'register_teacher.html', {'error_message': error_message})


def register_student(request):
    departments = Department.objects.all()
    allinstitutions = Institution.objects.all()
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name').lower()
        last_name = request.POST.get('last_name').lower()
        department_name = request.POST.get('department')
        email = request.POST.get('email').lower()
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        school = request.POST.get('institution').lower()  # Assuming this is passed as an ID or string
        profile_pic = request.FILES.get('profilepic')  # Retrieve the uploaded image
        print("profile_pic.name")


        # Initialize storage
        storage = SupabaseStorage()

        # Handle image upload
        image_url = None
        if profile_pic:
            post = 'media/' + profile_pic.name
            print(profile_pic.name)
            try:
                filename = storage.save(post, profile_pic)
                image_url = storage.url(filename)
            except Exception as e:
                error_message = "Failed to upload image to Supabase storage. Please try again."
                print(f"Error uploading image: {e}")

        # Basic validation
        if username and password and school and first_name and last_name and department_name and email:
            # Fetch the Department instance
            department = get_object_or_404(Department, name=department_name)

            # Create the user and student records
            user = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name, email=email)
            user.save()

            # Create Student instance, including the profile picture if uploaded
            student = Student(
                user=user,
                department=department,
                school=school,
                image=image_url  # Store the image URL instead of the file
            )
            student.save()
            login(request, user)

            return redirect('myprofile')
        else:
            error_message = "All fields are required."

    return render(request, 'register_student.html', {'error_message': error_message, 'alldepartments': departments, 'allinstitutions':allinstitutions})






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
def list_courses(request, department_id=None):
    if department_id:
        department = get_object_or_404(Department, id=department_id)
        courses = department.courses.all()  # Access courses through the related_name
    return render(request, 'list_courses.html', {'courses': courses, "department": department})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()
    return render(request, 'course_detail.html', {'course': course, 'topics': topics})


@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'topic_detail.html', {'topic': topic})



@login_required
def myprofile(request):
    user = request.user.username
    courses = Course.objects.all()
    return render(request, 'myprofile.html',{'user': user,'courses': courses} )


@login_required
def cbt_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = CBTQuestion.objects.filter(course=course)

    if request.method == 'POST':
        # Handle answer submission and scoring
        score = 0
        total_questions = questions.count()
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

        # Calculate percentage score for this attempt
        percentage_score = (score / total_questions) * 100

        # Update the course's percentage field
        # If this is the first attempt, set the percentage directly
        if course.percentage is None:
            course.percentage = percentage_score
        else:
            # Calculate new average if there is already a stored percentage
            course.percentage = (float(course.percentage) + percentage_score) / 2

        course.save()

        # Prepare context for the result page
        context = {
            'course': course,
            'score': score,
            'percentage_score': percentage_score,
            'total_questions': total_questions,
        }
        return render(request, 'cbt_result.html', context)

    # For GET request: render the questions template
    context = {
        'course': course,
        'questions': questions,
    }
    return render(request, 'cbt.html', context)


def all_past_questions(request):
    pastquestions = PastQuestions.objects.all()
    return render(request, 'cool/allpqs.html', {"pastquestions": pastquestions})

def past_questions(request, pastpq_id):
    pastpq = get_object_or_404(PastQuestions, id=pastpq_id)
    return render(request, 'pastquestions.html', {"pastpq": pastpq})


@login_required
def key_points(request, pastpq_id):
    pastpq = get_object_or_404(PastQuestions, id=pastpq_id)
    keypoint = KeyPoints.objects.filter(past_question=pastpq).first()  # Use .first() to fetch the single object

    return render(request, 'cool/keypoints.html', {'keypoint': keypoint})

