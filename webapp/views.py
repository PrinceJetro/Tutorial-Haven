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
import smtplib
import ssl





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
    departments = Department.objects.all()
    allinstitutions = TutorialCenter.objects.all()
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip().lower()
        last_name = request.POST.get('last_name', '').strip().lower()
        department_name = request.POST.get('department', '').strip()
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()
        school_id = request.POST.get('institution', '').strip().lower()  # School name or ID
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
        if username and password and school_id and first_name and last_name and department_name and email:
            try:
                # Fetch the Department instance
                department = get_object_or_404(Department, name=department_name)

                # Fetch the Institution instance
                institution = get_object_or_404(TutorialCenter, id=school_id)

                # Create the user
                user = User(
                    username=username,
                    password=make_password(password),
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                user.save()

                # Create the Student record
                student = Student(
                    user=user,
                    department=department,
                    tutorial_center=institution,  # Use the Institution instance
                    image=image_url,  # Store the image URL instead of the file
                )
                student.save()

                # Log the user in and redirect to their profile
                login(request, user)
                send_registration_email(
                    full_name=f"{first_name.title()} {last_name.title()}",
                    email=user.email,
                    institution_email=institution.owner.email
                )
                return redirect('myprofile')
               

            except Exception as e:
                error_message = f"An error occurred: {e}"
                print(f"Error: {e}")
        else:
            error_message = "All fields are required."

    return render(
        request,
        'register_student.html',
        {
            'error_message': error_message,
            'alldepartments': departments,
            'allinstitutions': allinstitutions,
        }
    )

def send_registration_email(full_name, email, institution_email):
    sender_email = 'princejetro123@gmail.com'
    sender_password = "iatu bier ypec yeqq"  # App password, not actual email password
    subject = "New Student Registration"
    body = f"""
Hello Tutorial Center Administration,

A new student has successfully registered. Here are the details:

Full Name: {full_name}
Email: {email}

Please review and approve their registration.

Best regards,
Tutorial Haven Team
"""

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, institution_email, f"Subject: {subject}\n\n{body}")
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def loginview(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST["username"],
                            password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('myprofile')
    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutor, Student, TutorialCenter
import smtplib
import ssl

@login_required
def approve_users(request):
    # Fetch the TutorialCenter owned by the logged-in user
    tutorial_center = get_object_or_404(TutorialCenter, owner=request.user)
    unapproved_tutors = Tutor.objects.filter(tutorial_center=tutorial_center, is_approved=False)
    unapproved_students = Student.objects.filter(tutorial_center=tutorial_center, is_approved=False)

    if request.method == 'POST':
        # Retrieve IDs of selected tutors and students for approval
        approved_tutor_ids = request.POST.getlist('approve_tutors')
        approved_student_ids = request.POST.getlist('approve_students')

        # Approve tutors
        for tutor in Tutor.objects.filter(id__in=approved_tutor_ids):
            tutor.is_approved = True
            tutor.save()
            send_approval_email(tutor.user.first_name, tutor.user.email, tutorial_center.name, "Tutor")

        # Approve students
        for student in Student.objects.filter(id__in=approved_student_ids):
            student.is_approved = True
            student.save()
            send_approval_email(student.user.first_name, student.user.email, tutorial_center.name, "Student")

        return redirect('approve_users')

    return render(request, 'approve_users.html', {
        'unapproved_tutors': unapproved_tutors,
        'unapproved_students': unapproved_students,
    })


def send_approval_email(first_name, email, institution_name, role):
    sender_email = 'princejetro123@gmail.com'
    sender_password = "iatu bier ypec yeqq"  # App password, not actual email password
    subject = "Account Approval Notification"
    body = f"""
Hello {first_name},

Congratulations! Your registration as a {role} at {institution_name} has been approved. You can now log in to your account and start engaging with the platform.

If you have any questions, feel free to contact us.

Best regards,
{institution_name} Team
"""

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, email, f"Subject: {subject}\n\n{body}")
        print(f"Approval email sent to {email}.")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")


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

    # Safely query for the tutorial center
    tutorial_center = TutorialCenter.objects.filter(owner=request.user).first()

    if tutorial_center:  # Check if the tutorial center exists
        approved_tutors = Tutor.objects.filter(tutorial_center=tutorial_center, is_approved=True)
        approved_students = Student.objects.filter(tutorial_center=tutorial_center, is_approved=True)

        return render(request, 'myprofile.html', {
            'user': user,
            'courses': courses,
            'approved_students': approved_students,
            'approved_tutors': approved_tutors,
        })
    else:
        # Render without tutorial center-specific data
        return render(request, 'myprofile.html', {
            'user': user,
            'courses': courses,
        })


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

