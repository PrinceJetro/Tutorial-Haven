# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import  Student, Course, Department, Topic,CBTQuestion, TutorialCenter, PastQuestions, KeyPoints, Tutor
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

