# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import  Student, Course, Department, Topic, TutorialCenter, PastQuestionsObj, KeyPoints, Tutor, PastQuestionsTheory, ObjGrade,TheoryGrade, UserCourseProgress, UploadedImage,  Achievement, UserAchievement, UserProgress, DiscussionForum, Comment, CustomQuestion, CustomQuestionResponse, UploadedImageCustom, ActivityLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db.models import Avg
from webapp.storage import SupabaseStorage
from .forms import TheorySubmissionForm, GradeForm, SearchForm, CustomSubmissionForm, CustomGrade
import smtplib
import ssl
from django.db.models import Avg  # Import Avg for aggregation
import uuid  # Ensure you have imported this at the top of the file
from django.contrib import messages  # Import messages for feedback to users
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Q
from functools import wraps
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os
import markdown
from random import shuffle





# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



def user_approved_required(view_func):
    """Decorator to check if a user is approved based on their role."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            # Redirect unauthenticated users to the login page
            return redirect('login')

        # Check if the user is a student and is approved
        if hasattr(user, 'student') and not user.student.is_approved:
            return HttpResponseForbidden("Your account has not been approved yet.")

        # Check if the user is a tutor and is approved
        if hasattr(user, 'tutor') and not user.tutor.is_approved:
            return HttpResponseForbidden("Your account has not been approved yet.")

        # Allow institutions without requiring approval
        if hasattr(user, 'tutorial_center') and user.tutorial_center.is_active:
            return view_func(request, *args, **kwargs)
        
        if hasattr(user, 'tutor') and user.tutor.is_approved and user.tutor.tutorial_center.is_active:
            return view_func(request, *args, **kwargs)

        if hasattr(user, 'student') and user.student.is_approved and user.student.tutorial_center.is_active:
            return view_func(request, *args, **kwargs)


        # If the user doesn't fit any valid role, deny access
        return HttpResponseForbidden("Access denied.")

    return _wrapped_view





def home(request):
    return render(request, "cool/index.html")




def register_owner(request):
    error_message = ""

    if request.method == 'POST':
        # Retrieve and clean input fields
        first_name = request.POST.get('first_name', '').strip().lower()
        last_name = request.POST.get('last_name', '').strip().lower()
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip().lower()
        tutorial_center_name = request.POST.get('tutorial_center_name', '').strip().lower()
        tutorial_center_address = request.POST.get('tutorial_center_address', '').strip().lower()
        tutorial_center_discipline = request.POST.get('tutorial_center_discipline', '').strip().lower()
        profile_pic = request.FILES.get('profilepic')

        # Input validation: ensure all required fields are provided
        if not (username and password and tutorial_center_name):
            messages.error(request, "All fields are required.")
            return render(request, 'register_owner.html', {'error_message': "All fields are required."})

        # Check for existing username, email, or institution
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register_owner.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register_owner.html')

        if TutorialCenter.objects.filter(name=tutorial_center_name).exists():
            messages.error(request, "Institution is already registered.")
            return render(request, 'register_owner.html')

        # Upload profile image to Supabase (optional)
        storage = SupabaseStorage()
        image_url = None
        if profile_pic:
            try:
                storage_path = f"media/{profile_pic.name}"
                filename = storage.save(storage_path, profile_pic)
                image_url = storage.url(filename)
                print(f"Profile image uploaded: {image_url}")
            except Exception as e:
                error_message = "Failed to upload image to storage."
                print(f"Error uploading image: {e}")
                messages.error(request, error_message)
                return render(request, 'register_owner.html', {'error_message': error_message})

        # Create and save user
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=make_password(password)
            )
            # Create and save tutorial center
            tutorial_center = TutorialCenter.objects.create(
                name=tutorial_center_name,
                owner=user,
                address=tutorial_center_address,
                desc=tutorial_center_discipline,
                image=image_url
            )

            # Log the user in and redirect
            login(request, user)
            return redirect('myprofile')
        except Exception as e:
            error_message = "Error creating account. Please try again."
            print(f"Error saving user or tutorial center: {e}")
            messages.error(request, error_message)
            return render(request, 'register_owner.html', {'error_message': error_message})

    # Render registration form
    return render(request, 'register_owner.html', {'error_message': error_message})



def register_tutor(request):
    allinstitutions = TutorialCenter.objects.all()
    allcourses = Course.objects.all()
    error_message = ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip().lower()
        last_name = request.POST.get('last_name', '').strip().lower()
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()
        school_id = request.POST.get('institution', '').strip().lower()  # School name or ID
        course_ids = request.POST.getlist('course')
        profile_pic = request.FILES.get('profilepic')  # Retrieve the uploaded image

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register_tutor.html',{
            'error_message': error_message,
            'allinstitutions': allinstitutions,
        })
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register_tutor.html',{
            'error_message': error_message,
            'allinstitutions': allinstitutions,
        })

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
        if username and password and school_id and first_name and last_name  and email:
            try:
                # Fetch the Institution and Course instance
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

                # Create the Tutor record
                tutor = Tutor(
                    user=user,
                    tutorial_center=institution,  # Use the Institution instance
                    image=image_url,  # Store the image URL instead of the file
                )
                tutor.save()
                tutor.speciality.set(course_ids)


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
        'register_tutor.html',
        {
            'error_message': error_message,
            'allinstitutions': allinstitutions,
            'allcourses': allcourses,
        }
    )

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

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'register_student.html',{
            'error_message': error_message,
            'alldepartments': departments,
            'allinstitutions': allinstitutions,
        })
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register_student.html',{
            'error_message': error_message,
            'alldepartments': departments,
            'allinstitutions': allinstitutions,
        })

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
https://tutorialhaven.vercel.app/approve-users

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
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('myprofile')
        else:
            # Add error message for invalid credentials
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


@login_required
@user_approved_required
def delete_student(request, student_id):
    print("called")
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        # student.delete()
        messages.success(request, "Student deleted successfully.")
        print("Student deleted successfully.")
        return redirect('list_tutorial_students', tutorial_id=request.user.tutorial_center.id) 
        

@user_approved_required
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
            
            # Prefill UserCourseProgress if missing
            try:
                department_courses = student.department.courses.all()
                for course in department_courses:
                    # Create or retrieve progress records for the student
                    UserCourseProgress.objects.get_or_create(user=student.user, course=course)
            except Exception as e:
                # Log the error (replace print with proper logging in production)
                print(f"Error pre-filling UserCourseProgress for {student.user.username}: {e}")

            send_approval_email(student.user.first_name, student.user.email, tutorial_center.name, "Student")

        return redirect('approve_users')

    return render(request, 'approve_users.html', {
        'unapproved_tutors': unapproved_tutors,
        'unapproved_students': unapproved_students,
    })


@login_required
@user_approved_required
def delete_user_registration(request):
    pass



def send_approval_email(first_name, email, institution_name, role):
    sender_email = 'princejetro123@gmail.com'
    sender_password = "iatu bier ypec yeqq"  # App password, not actual email password
    subject = "Account Approval Notification"
    body = f"""
Hello {first_name},

Congratulations! Your registration as a {role} at {institution_name} has been approved. You can now log in to your account and start engaging with the platform.
https://tutorialhaven.vercel.app/myprofile
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


@user_approved_required
@login_required
def list_departments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "cool/departments.html", {"departments": departments})


@user_approved_required
@login_required
def list_all_courses(request):
    all_courses = Course.objects.order_by('name').all()
    return render(request, 'list_courses.html', {'courses': all_courses})


@user_approved_required
@login_required
def list_courses(request, department_id=None):
    if department_id:
        department = get_object_or_404(Department, id=department_id)
        courses = department.courses.all()  # Access courses through the related_name
    return render(request, 'list_courses.html', {'courses': courses, "department": department})


@user_approved_required
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()  # Order related topics alphabetically by 'name'
    userprogress = UserCourseProgress.objects.filter(user=request.user, course=course).first()

    return render(
        request, 
        'course_detail.html', 
        {'course': course, 'topics': topics, 'userprogress': userprogress}
    )
 
from django.http import JsonResponse
import json

@user_approved_required
@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == "POST":
        # Parse JSON data from the request
        try:
            data = json.loads(request.body)  # Parse JSON body
            user_message = data.get('message', '')  # Extract the user message
            topic_content = topic.content
            openai.api_key = api_key
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an expert tutor on the topic: {topic.name}. Answer based only on this topic."},
                    {"role": "assistant", "content": topic_content},
                    {"role": "user", "content": user_message},
                ]
            )
            ai_reply = response.choices[0].message.content.replace("\n", "<br>").replace("---", "<hr>")

            return JsonResponse({"reply": ai_reply})  # Return AI's reply as JSON
        except Exception as e:
            print(f"Error: {e}")  # Log errors for debugging
            return JsonResponse({"reply": "Sorry, I couldn't process your request."}, status=500)

    return render(request, 'topic_detail.html', {'topic': topic})


@login_required
def myprofile(request):
    user = request.user.username
    courses = Course.objects.all().order_by("name")[:5]

    # Safely query for the tutorial center and tutor
    tutorial_center = TutorialCenter.objects.filter(owner=request.user).first()
    tutor = Tutor.objects.filter(user=request.user).first()

    if tutorial_center:  # Check if the user owns a tutorial center
        approved_tutors = Tutor.objects.filter(tutorial_center=tutorial_center, is_approved=True).order_by('-id')[:5]
        approved_students = Student.objects.filter(tutorial_center=tutorial_center, is_approved=True).order_by('-id')[:5]

        return render(request, 'myprofile.html', {
            'user': user,
            'courses': courses,
            'approved_students': approved_students,
            'approved_tutors': approved_tutors,
        })

    if tutor:  # Check if the user is a tutor
        # Get the tutorial center associated with the tutor
        tutorial_center = tutor.tutorial_center
        approved_students = Student.objects.filter(tutorial_center=tutorial_center, is_approved=True).order_by('-id')[:5]

        return render(request, 'myprofile.html', {
            'user': user,
            'courses': courses,
            'approved_students': approved_students,
        })

    # If neither tutorial center owner nor tutor
    return render(request, 'myprofile.html', {
        'user': user,
        'courses': courses,
    })


@user_approved_required
@login_required
def list_tutorial_students(request, tutorial_id):
    # Get the tutorial center by name or return 404 if not found
    center = get_object_or_404(TutorialCenter, id=tutorial_id)
    
    # Check if the user is the owner or an approved tutor associated with the center
    if request.user != center.owner and not Tutor.objects.filter(user=request.user, tutorial_center=center, is_approved=True).exists():
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Get only approved students associated with the center
    students = center.students.filter(is_approved=True)

    return render(request, 'tutorial_students.html', {'students': students, 'center': center})


@user_approved_required
@login_required
def cbtquestion(request, course_id):
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    # Load environment variables from .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    course = get_object_or_404(Course, id=course_id)
    questions = PastQuestionsObj.objects.filter(course=course)[:10]

    if request.method == 'POST':
        if hasattr(request.user, 'tutorial_center') or hasattr(request.user, 'tutor'):
            messages.success(request, "Practice session has been successfully received. However, submissions are restricted for staff accounts.")
            return HttpResponseRedirect('/allcourses/')
        
        score = 0
        total_questions = questions.count()
        failed_questions = []
        submission_id = uuid.uuid4()  # Generate a unique submission ID for this attempt

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            print(selected_option)
            correct_option = question.correct_option
            # Get actual text for selected and correct options
            selected_option_text = getattr(question, f"option_{(selected_option.lower() if selected_option else '')}", '')
            correct_option_text = getattr(question, f"option_{correct_option.lower()}")

            if selected_option == question.correct_option:
                score += 1
                # print(f"Got {question.question_text}")
                # print(f"{selected_option_text} is correct")
            else:
                # Append failed question details
                # print(f"Failed {question.question_text}")
                # print(f"{selected_option_text} was picked")

                failed_questions.append({
                    "question_text": question.question_text,
                    "selected_option": selected_option_text,
                })

            # Save individual grade for this question
            ObjGrade.objects.create(
                user=request.user,
                question=question,
                course=course,
                score=100 if selected_option == question.correct_option else 0,
                submission_id=submission_id,  # Assign the unique submission ID
            )

        # Handle failed questions via OpenAI API
        if failed_questions:
            try:
                # Format failed questions into a prompt
                failed_prompt = "\n".join([
                    f"Question: {fq['question_text']}\nYour Answer: {fq['selected_option']}"
                    for fq in failed_questions
                ])
                
                # Call the OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a tutor reviewing a student's answers. For each question, critically evaluate the correctness of the provided answers, even if marked as 'correct.' If you find discrepancies or potential inaccuracies, provide the most accurate answer with explanations. For incorrect answers, explain why they are wrong, clarify the correct answer, and suggest how the student can improve.           If your explanation involves any formula, mathematical expression, or chemical equation, make sure to provide it in LaTeX format. For display math, use double dollar signs like this: $$ E = mc^2 $$ and for inline math, use \\( E = mc^2 \\). Provide the raw LaTeX code, not the rendered output, so that it can be rendered properly on the frontend using MathJax or LaTeX rendering tools. For chemical equations, use proper LaTeX formatting such as \\( \\text{H}_2\\text{O} \\) for water. "},
                        {"role": "user", "content": f"The following are the questions I failed:\n\n{failed_prompt}"}
                    ],
                    temperature=0.3,
                    max_completion_tokens=3500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                # Extract and prepare response content
                tutor_feedback = response.choices[0].message.content.replace("\n", "<br>").replace("---", "<hr>")
            except Exception as e:
                tutor_feedback = f"An error occurred while generating feedback: {str(e)}"
        else:
            # If no failed questions, generate perfect score feedback
            tutor_feedback = """
    <h2>Congratulations!</h2>
    <p>You scored a perfect grade! Well done! 🎉</p>
    <p>Since you achieved a perfect score, you've unlocked the "Ace the Test" achievement! Keep up the great work and continue challenging yourself!</p>
    <p>Your dedication to studying has paid off. Keep up the momentum and aim for even greater achievements!</p>
    """

        # Calculate overall percentage score for this attempt
        percentage_score = (score / total_questions) * 100

        # Check for "Perfect Grade" achievement
        if percentage_score == 100:
            progress, created = UserProgress.objects.get_or_create(user=request.user)
            progress.exams_perfect_score += 1
            progress.save()

            achievement = Achievement.objects.filter(name="Ace the Test").first()
            if achievement:
                user_achievement, created = UserAchievement.objects.get_or_create(
                    user=request.user,
                    achievement=achievement
                )
                if created:
                    messages.success(request, "Congratulations! You've unlocked the 'Ace the Test' achievement!")

        # Update or create the user's progress for this course
        user_progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
        )
        user_progress.attempts += 1
        all_user_grades = ObjGrade.objects.filter(user=request.user, course=course)
        average_score = all_user_grades.aggregate(average_score=Avg('score'))['average_score'] or 0
        user_progress.percentage = average_score
        user_progress.save()

        # Redirect to a results page or display results
        context = {
            'course': course,
            'score': score,
            'percentage_score': percentage_score,
            'total_questions': total_questions,
            'attempts': user_progress.attempts,
            'total_percent': user_progress.percentage,
            'tutor_feedback': tutor_feedback
        }
        ActivityLog.objects.create(
            user=request.user,
            action=f"Practiced CBT questions for the course '{course.name}'. Scored {percentage_score:.2f}% with {score}/{total_questions} correct answers."
        )
        return render(request, 'cbt_result.html', context)

    context = {
        'course': course,
        'cbt_questions': questions,
    }
    return render(request, 'pastquestion.html', context)

@user_approved_required
@login_required
def listTheory(request):
    theories = PastQuestionsTheory.objects.order_by('course').all()
    return render(request, 'list_theory.html', {
        'theories':theories
    })


@user_approved_required
@login_required
def theoryquestion(request, course_id, year):
    course = get_object_or_404(Course, id=course_id)
    questions = PastQuestionsTheory.objects.filter(course=course, year=year).first()

    if request.method == 'POST':
        print(request.POST)  # Debugging: Print POST data
        uploaded_images = request.FILES.getlist("images")  # Retrieve uploaded images
        form = TheorySubmissionForm(request.POST)

        if form.is_valid():  # Ensure the form is valid
            response = form.cleaned_data['response']
            question_id = request.POST.get('question_id')
            question = get_object_or_404(PastQuestionsTheory, id=question_id)

            # Prevent staff submissions
            if hasattr(request.user, 'tutorial_center') or hasattr(request.user, 'tutor'):
                messages.success(request, f"{questions} have been successfully received. However, submissions are restricted for staff accounts.")
                return HttpResponseRedirect('/all_theories')

            # Create TheoryGrade instance
            theory_grade = TheoryGrade.objects.create(
                user=request.user,
                question=question,
                question_text=question.question_text,
                course=course,
                response=response,
                submission_id=uuid.uuid4()
            )

            # Initialize storage for image upload
            storage = SupabaseStorage()
            try:
                print("Uploading images...")
                for image in uploaded_images:
                    # Define storage path
                    storage_path = f"diagrams/{image.name}"
                    print(f"Uploading file: {image.name}")

                    # Save to Supabase and get URL
                    filename = storage.save(storage_path, image)
                    image_url = storage.url(filename)

                    # Save image record to UploadedImage model
                    UploadedImage.objects.create(theory_grade=theory_grade, image=image_url)
                print("Images uploaded successfully.")
            except Exception as e:
                print(f"Error uploading images: {e}")
                messages.error(request, "Failed to upload one or more images. Please try again.")

            # Send email notification to tutor
            tutor = Tutor.objects.filter(speciality=course).first()
            if tutor and tutor.user.email:
                sender_email = 'princejetro123@gmail.com'
                sender_password = "iatu bier ypec yeqq"
                recipient_email = tutor.user.email
                subject = "New Theory Practice Submission"
                body = f"""
Dear {tutor.user.username},

A new theory practice response has been submitted by {request.user.get_full_name()} for the course '{course.name}'.

Please log in to your dashboard to review and grade the submission.

Best regards,
Tutorial Haven Tech Team
"""

                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(sender_email, sender_password)
                        smtp.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
                        print(f"Notification email sent to {tutor.user.email}.")
                except Exception as e:
                    print(f"Failed to send email to {tutor.user.email}: {e}")

            # Success message and redirect
            messages.success(request, f"{questions} Successfully Submitted! Your Tutor will grade and get back to you soon.")
            ActivityLog.objects.create(
            user=request.user,
            action=f"Practiced Theory questions for {question.year} {course.name}"
            )
            return HttpResponseRedirect('/all_theories')
        else:
            # Form validation error
            messages.error(request, "Answers Cannot Be Blank. You must submit an answer.")
    else:
        form = TheorySubmissionForm()

    context = {
        'course': course,
        'theory_questions': questions,
        'form': form,
    }
    return render(request, 'theoryquestion.html', context)


@user_approved_required
@login_required
def list_pending_theory(request, tutor_id):
    # Get the logged-in tutor
    tutor = get_object_or_404(Tutor, user=request.user)

    # Get all the tutor's specialities (courses)
    speciality_courses = tutor.speciality.all()
    # Fetch all pending grades for the tutor's courses
    pending_grades = TheoryGrade.objects.filter(course_id__in=speciality_courses, score=0)
    # Pass the data to the template
    context = {
        'pending_grades': pending_grades,
        'courses': speciality_courses,  # Pass all courses for the tutor
    }
    return render(request, 'pending_grades.html', context)


@user_approved_required
@login_required
def all_pending_theory(request):
    pending_grades = TheoryGrade.objects.filter(score=0)
    courses = Course.objects.all()
    # Pass the data to the template
    context = {
        'pending_grades': pending_grades,
        'courses': courses,  # Pass all courses for the tutor
    }
    return render(request, 'pending_grades.html', context)

@user_approved_required
@login_required
def grade_theory(request, grade_id):
    # Fetch the TheoryGrade object
    theory_grade = get_object_or_404(TheoryGrade, id=grade_id)
    images = UploadedImage.objects.filter(theory_grade=theory_grade)  # Retrieve all related images

    # Ensure the user has the right to grade
    if not (hasattr(request.user, 'tutor') and request.user.tutor) and not (hasattr(request.user, 'tutorial_center') and request.user.tutorial_center):
        messages.error(request, "You do not have permission to grade this question.")
        return redirect('myprofile')  # Redirect to a suitable page

    # Handle form submission
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=theory_grade)
        if form.is_valid():
            form.save()  # Save the updated score
            ActivityLog.objects.create(
            user=request.user,
            action=f"Graded Theory Question for {theory_grade.user} {theory_grade.question.year}"
            )
            messages.success(request, "Score updated successfully!")
             # Redirect based on user type
            if hasattr(request.user, 'tutor') and request.user.tutor:
                return redirect('pending_gradings', tutor_id=request.user.tutor.id)
            elif hasattr(request.user, 'tutorial_center') and request.user.tutorial_center:
                return redirect('all_pending_gradings')
            else:
                return redirect('myprofile')  # Fallback in case of unexpected user type


                

    else:
        form = GradeForm(instance=theory_grade)

    # Pass data to the template
    context = {
        'theory_grade': theory_grade,
        'form': form,
        'images': images,  # Pass all images to the template
    }
    return render(request, 'grade_theory.html', context)

# Utility function to calculate credits
def calculate_credits(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    elif percentage == 0:
        return "_____"
    else:
        return "F"



@user_approved_required
@login_required
def myreport(request):
    objgrades = UserCourseProgress.objects.filter(user=request.user).order_by('-percentage')
    theorygrades = TheoryGrade.objects.filter(user=request.user).order_by('-submitted_at')
    customgrades = CustomQuestionResponse.objects.filter(student=request.user).order_by('-submitted_at')


    graded_data = []
    graded_data_theory = []
    graded_data_custom = []

    # Summarize performance data
    overall_performance = {"total_courses": 0, "average_percentage": 0, "strengths": [], "weaknesses": []}
    total_percentage = 0
    total_courses = 0

    for grade in objgrades:
        credits = calculate_credits(grade.percentage)
        graded_data.append({
            "course": grade.course.name,
            "percentage": grade.percentage,
            "credits": credits,
            "attempts": grade.attempts,
        })

        # Include only attempted courses in the total percentage and course count
        if grade.percentage != 0:
            total_percentage += grade.percentage
            total_courses += 1


    for grade in theorygrades:
        credits = calculate_credits(grade.score)
        graded_data_theory.append({
            "course": grade.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "year": grade.question.year,
        })

    for grade in customgrades:
        credits = calculate_credits(grade.score)
        graded_data_custom.append({
            "course": grade.question.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "title": grade.question.title,
        })

    # Calculate aggregated performance
    if total_courses > 0:
        overall_performance["total_courses"] = total_courses
        overall_performance["average_percentage"] = round(total_percentage / total_courses, 2)

        # Identify strengths and weaknesses
        strengths = [grade for grade in objgrades if grade.percentage > 75]
        weaknesses = [grade for grade in objgrades if grade.percentage < 50]

        overall_performance["strengths"] = [s.course.name for s in strengths]
        overall_performance["weaknesses"] = [w.course.name for w in weaknesses]

    # Generate AI feedback
    feedback_prompt = (
        f"Student Name: {request.user.username}\n\n"
        f"Performance Summary:\n"
        f"- Total Courses: {overall_performance['total_courses']}\n"
        f"- Average Percentage: {overall_performance['average_percentage']}%\n\n"
        f"Strengths:\n{', '.join(overall_performance['strengths'])}\n\n"
        f"Weaknesses:\n{', '.join(overall_performance['weaknesses'])}\n\n"
        """Based on this data, provide detailed feedback on the my performance. Include:
            Performance Analysis: Trends, strengths, and areas needing improvement.
            Strengths & Weaknesses: Key abilities to leverage and gaps to address with constructive suggestions.
            Actionable Strategies: Practical steps and study techniques for improvement.
            Resources: Recommend tailored tools like courses, books, or practice materials.
            Behavioral Insights: Comment on engagement, consistency, or mindset, with advice for improvement.
            Progress Tracking: Suggest ways to measure and monitor improvement.
            Encouragement: End with motivational advice to inspire confidence and growth.
            Keep the tone clear, professional, and empathetic to support both me and my mentor."""
    )

    ai_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tutor providing a detailed student progress report with actionable insights for me. End by saying 'Best regards, TH-AI'"},
            {"role": "user", "content": feedback_prompt},
        ],
        temperature=0.7,
        max_tokens=2500,
    )
    ai_feedback = ai_response.choices[0].message.content.replace("\n", "<br>").replace("---", "<hr>")

    context = {
        "graded_data": graded_data,
        "graded_data_theory": graded_data_theory,
        "graded_data_custom": graded_data_custom,
        "overall_performance": overall_performance,
        "ai_feedback": ai_feedback,
    }
    return render(request, 'report.html', context)


@user_approved_required
@login_required
def studentsreport(request, student_id):
    # Fetch student data
    student = get_object_or_404(Student, id=student_id)
    objgrades = UserCourseProgress.objects.filter(user=student.user).order_by('-percentage')
    theorygrades = TheoryGrade.objects.filter(user=student.user).order_by('-score')
    customgrades = CustomQuestionResponse.objects.filter(student=student.user).order_by('-score')

    graded_data = []
    graded_data_theory = []
    graded_data_custom = []

    # Summarize performance data
    overall_performance = {"total_courses": 0, "average_percentage": 0, "strengths": [], "weaknesses": []}
    total_percentage = 0
    total_courses = 0

    for grade in objgrades:
        credits = calculate_credits(grade.percentage)
        graded_data.append({
            "course": grade.course.name,
            "percentage": grade.percentage,
            "credits": credits,
            "attempts": grade.attempts,
        })

        # Include only attempted courses in the total percentage and course count
        if grade.percentage != 0:
            total_percentage += grade.percentage
            total_courses += 1


    for grade in theorygrades:
        credits = calculate_credits(grade.score)
        graded_data_theory.append({
            "course": grade.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "year": grade.question.year,
        })

    for grade in customgrades:
        credits = calculate_credits(grade.score)
        graded_data_custom.append({
            "course": grade.question.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "title": grade.question.title,
        })

    # Calculate aggregated performance
    if total_courses > 0:
        overall_performance["total_courses"] = total_courses
        overall_performance["average_percentage"] = round(total_percentage / total_courses, 2)

        # Identify strengths and weaknesses
        strengths = [grade for grade in objgrades if grade.percentage >= 60]
        weaknesses = [grade for grade in objgrades if 0 < grade.percentage < 60]

        overall_performance["strengths"] = [s.course.name for s in strengths]
        overall_performance["weaknesses"] = [w.course.name for w in weaknesses]

    # Generate AI feedback
    feedback_prompt = (
        f"Student Name: {student.user.username}\n\n"
        f"Performance Summary:\n"
        f"- Total Courses: {overall_performance['total_courses']}\n"
        f"- Average Percentage: {overall_performance['average_percentage']}%\n\n"
        f"Strengths:\n{', '.join(overall_performance['strengths'])}\n\n"
        f"Weaknesses:\n{', '.join(overall_performance['weaknesses'])}\n\n"
        """Based on this data, provide detailed feedback on the student's performance. Include:
            Performance Analysis: Trends, strengths, and areas needing improvement.
            Strengths & Weaknesses: Key abilities to leverage and gaps to address with constructive suggestions.
            Actionable Strategies: Practical steps and study techniques for improvement.
            Resources: Recommend tailored tools like courses, books, or practice materials.
            Behavioral Insights: Comment on engagement, consistency, or mindset, with advice for improvement.
            Progress Tracking: Suggest ways to measure and monitor improvement.
            Encouragement: End with motivational advice to inspire confidence and growth.
            Keep the tone clear, professional, and empathetic to support both the student and their mentor."""
    )

    ai_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tutor providing a detailed student progress report with actionable insights."},
            {"role": "user", "content": feedback_prompt},
        ],
        temperature=0.7,
        max_tokens=2500,
    )
    ai_feedback = ai_response.choices[0].message.content.replace("\n", "<br>").replace("---", "<hr>")

    context = {
        "student": student,
        "graded_data": graded_data,
        "graded_data_theory": graded_data_theory,
        "graded_data_custom": graded_data_custom,
        "overall_performance": overall_performance,
        "ai_feedback": ai_feedback,
    }

    return render(request, 'studentsreport.html', context)





@user_approved_required
@login_required
def key_points(request, pastpq_id):
    pastpq = get_object_or_404(PastQuestionsObj, id=pastpq_id)
    keypoint = KeyPoints.objects.filter(past_question=pastpq).first()  # Use .first() to fetch the single object
    return render(request, 'cool/keypoints.html', {'keypoint': keypoint})




@login_required
def search(request):
    query = request.GET.get('query', '')  # Get the search query from the URL
    results = []

    if query:
        # Search in Topic model
        topic_results = Topic.objects.filter(name__icontains=query)  # Adjust this filter based on your field names
        for topic in topic_results:
            results.append({'object': topic, 'type': 'Topic'})

        # Search in PastQuestionObj model
        pastquestionobj_results = PastQuestionsObj.objects.filter(question_text__icontains=query)  # Adjust based on field names
        for past_question in pastquestionobj_results:
            results.append({'object': past_question, 'type': 'PastQuestionObj'})
    
        # Search in PastQuestionTheory model
        pastquestiontheory_results = PastQuestionsTheory.objects.filter(question_text__icontains=query)  # Adjust based on field names
        for past_question in pastquestiontheory_results:
            results.append({'object': past_question, 'type': 'PastQuestionTheory'})

    # If no query, show empty results
    return render(request, 'search_results.html', {
        'form': SearchForm(),  # Provide the search form
        'results': results,  # The search results
        'query': query,  # Pass the search query to show it in the template
    })

@user_approved_required
@login_required
def achievements_list(request):
    """List all achievements and user's unlocked achievements."""
    achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user)
    unlocked_ids = user_achievements.values_list('achievement_id', flat=True)

    context = {
        "achievements": achievements,
        "unlocked_ids": unlocked_ids,
        "user_achievements": user_achievements,
    }
    return render(request, "achievement_list.html", context)



def check_and_unlock_achievements(request, user):
    """Check all achievements and unlock those the user qualifies for."""
    progress = user.progress
    achievements = Achievement.objects.all()

    for achievement in achievements:
        if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            # Check specific achievement criteria
            if achievement.name == "First Step" and progress.topics_completed >= 1:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Congratulations! You unlocked the 'First Step' achievement.")

            elif achievement.name == "Course Enthusiast" and progress.courses_completed >= 5:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Great job! You unlocked the 'Course Enthusiast' achievement.")

            elif achievement.name == "Top Performer" and progress.exams_perfect_score >= 1:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Amazing! You unlocked the 'Top Performer' achievement.")

            elif achievement.name == "Course Master" and progress.courses_completed >= achievement.required_value:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, f"Incredible! You unlocked the 'Course Master' achievement.")

            elif achievement.name == "Social Learner" and progress.discussion_posts == 1:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "You unlocked the 'Social Learner' achievement for joining the discussion!")

            elif achievement.name == "Engaged Contributor" and progress.discussion_posts == 10:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Fantastic! You unlocked the 'Engaged Contributor' achievement.")

            elif achievement.name == "Community Leader" and progress.discussion_posts == 50:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Congratulations! You unlocked the 'Community Leader' achievement.")

            elif achievement.name == "Social Influencer" and progress.discussion_posts == 100:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Outstanding! You unlocked the 'Social Influencer' achievement.")

            elif achievement.name == "Discussion Master" and progress.discussion_posts == 500:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "Legendary! You unlocked the 'Discussion Master' achievement.")
            
            # Check for "Talk of the Town" achievement
            elif achievement.name == "Talk Of The Town":
                forums = DiscussionForum.objects.all()  # Assuming you have a Forum model
                for forum in forums:
                    if forum.comments.count() >= 50 and forum.creator == user:
                        UserAchievement.objects.create(user=user, achievement=achievement)
                        talk_of_the_town(forum)

            elif achievement.name == "Milestone Achiever" and UserAchievement.objects.filter(user=user).count() >= 10:
                UserAchievement.objects.create(user=user, achievement=achievement)
                messages.success(request, "You're unstoppable! You unlocked the 'Milestone Achiever' achievement.")


def talk_of_the_town(forum):
    sender_email = 'princejetro123@gmail.com'
    sender_password = "iatu bier ypec yeqq"  # App password, not actual email password
    subject = "Congratulations On the 'Talk Of The Town' achievement."
    body = f"""
Hello {forum.creator.username},

We are thrilled to inform you that your forum, titled "{forum.title}", has achieved an incredible milestone! With over 50 comments and counting, your forum has sparked meaningful discussions and interactions among our community members.

This remarkable achievement has unlocked the exclusive "Talk Of The Town" badge, a testament to your ability to create engaging and impactful content.

**Forum Details**:
- **Title**: {forum.title}
- **Total Comments**: {forum.comments.count()}
- **Created On**: {forum.created_at.strftime('%B %d, %Y')}

We encourage you to continue inspiring and engaging with the community. You can view your unlocked achievements in your profile section.

Thank you for your valuable contributions to our platform!

Best regards,  
Tutorial Haven Team  
"""
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, forum.creator.email, f"Subject: {subject}\n\n{body}")
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")






@user_approved_required
@login_required
def user_progress(request):
    """Display the user's current progress."""
    progress = get_object_or_404(UserProgress, user=request.user)
    return render(request, "achievement_progress.html", {"progress": progress})



@user_approved_required
@login_required
def complete_topic(request):
    if request.method == "POST":
        topic_id = request.POST.get("topic_id")
        print(topic_id)
        if not topic_id:
            return HttpResponseBadRequest("No topic specified.")
        
        # Get the topic and user's progress
        topic = get_object_or_404(Topic, id=topic_id)
        user = request.user
        progress, created = UserProgress.objects.get_or_create(user=user)

        # Check if the topic is already completed
        if progress.completed_topics.filter(id=topic.id).exists():
            return JsonResponse({"message": "Topic already completed.", "success": False})

        # Add topic to completed list and update count
        progress.completed_topics.add(topic)
        progress.topics_completed = progress.completed_topics.count()  # Update cached count
        progress.save()

        # Check for achievements
        check_and_unlock_achievements(user)

        return JsonResponse({"message": "Topic marked as completed.", "success": True})

    return HttpResponseBadRequest("Invalid request method.")

    
        # Check if the user has completed all topics in the course
        # course = topic.course
        # if progress.completed_topics.filter(course=course).count() == course.topics.count():
        #     # The user has completed all topics in the course - unlock the "Course Master" achievement
        #     achievement = Achievement.objects.filter(name="Course Master").first()
        #     if achievement:
        #         user_achievement, created = UserAchievement.objects.get_or_create(
        #             user=user,
        #             achievement=achievement
        #         )
        #         if created:
        #             messages.success(request, "Congratulations! You've unlocked the 'Course Master' achievement!")

        # # Check if the user has completed 5 courses - unlock the "Course Enthusiast" achievement
        # # First get all courses the user has completed by checking completed topics
        # completed_courses = UserCourseProgress.objects.filter(user=user)
        
        # completed_courses_with_topic_count = completed_courses.annotate(
        #     num_completed_topics=Count('course__topics', filter=Q(course__topics__in=progress.completed_topics))
        # )
        
        # # Count how many of these courses have all topics completed
        # completed_courses_count = completed_courses_with_topic_count.filter(
        #     num_completed_topics=F('course__topics__count')
        # ).count()

        # if completed_courses_count >= 5:
        #     achievement = Achievement.objects.filter(name="Course Enthusiast").first()
        #     if achievement:
        #         user_achievement, created = UserAchievement.objects.get_or_create(
        #             user=user,
        #             achievement=achievement
        #         )
        #         if created:
        #             messages.success(request, "Congratulations! You've unlocked the 'Course Enthusiast' achievement!")

        # Check for other achievements


@user_approved_required
@login_required
def forum_list(request):
    # Get the tutorial center of the current user
    if hasattr(request.user, 'tutor'):
        center = request.user.tutor.tutorial_center
    elif hasattr(request.user, 'tutorial_center'):
        print("here")
        center = request.user.tutorial_center
        print(center)
    elif hasattr(request.user, 'student'):
        center = request.user.student.tutorial_center
    else:
        center = None

    # If the user has an associated tutorial center, filter forums by it
    if center:
        forums = DiscussionForum.objects.select_related('course').all().order_by('-created_at')
    else:
        forums = DiscussionForum.objects.none()  # Return an empty queryset if no center found

    return render(request, "forums/forum_list.html", {"forums": forums})


@user_approved_required
@login_required
def forum_detail(request, forum_id):
    forum = get_object_or_404(DiscussionForum, id=forum_id)
    comments = forum.comments.all().order_by('-created_at')

    # Mock data: Replace these with actual course-related data from your models
    topics = forum.course.topics.all()
    theory_questions = forum.course.theory_questions.all()
    cbt_questions = forum.course.objective_questions.all()


    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(forum=forum, commenter=request.user, content=content)
        user = request.user
        progress, created  = UserProgress.objects.get_or_create(user=user)
        progress.discussion_posts += 1
        progress.save()

        # Check for achievements
        check_and_unlock_achievements(request,user)


        return redirect("forum_detail", forum_id=forum_id)

    return render(request, "forums/forum_detail.html", {
        "forum": forum,
        "comments": comments,
        "topics": topics,
        "theory_questions": theory_questions,
        "cbt_questions": cbt_questions,
    })


@user_approved_required
@login_required
def create_forum(request):
    courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title")
        content = request.POST.get("content")
        course = get_object_or_404(Course, id=course_id)
        DiscussionForum.objects.create(creator=request.user, course=course, title=title, content=content)
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created a Discussion Forum under the {course.name} course with title: {title}"
            )
        return redirect("forum_list")

    return render(request, "forums/create_forum.html", {"courses": courses})



@user_approved_required
@login_required
def delete_forum(request, forum_id):
    forum = get_object_or_404(DiscussionForum, id=forum_id)

    # # Ensure only the creator can delete the forum
    # if request.user != forum.creator:
    #     messages.error(request, "You are not authorized to delete this forum.")
    #     return redirect('forum_detail', forum_id=forum.id)

    # If the user is authorized, delete the forum
    if request.method == "POST":
        forum.delete()
        messages.success(request, "Forum deleted successfully.")
        return redirect('forum_list')  # Redirect to the forum list page after deletion

    # If the method is not POST, redirect back to the forum detail page
    messages.warning(request, "Invalid request method.")
    ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted a Discussion Forum under the {forum.course.name} course with title: {forum.title}"
            )
    return redirect('forum_detail', forum_id=forum.id)




@user_approved_required
@login_required
def create_custom_question(request):
    courses = Course.objects.all()

    if request.method == "POST":
        print(request.POST)
        # Ensure only tutors can create questions
        if not hasattr(request.user, 'tutor'):
            return HttpResponseForbidden("You do not have permission to create questions.")
        
        course_id = request.POST.get("course")
        tutor = request.user.tutor
        question_text = request.POST.get("response")
        title = request.POST.get("title")
        course = get_object_or_404(Course, id=course_id)
        CustomQuestion.objects.create(course=course, tutor=tutor, question_text=question_text,title=title)
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created a Custom {course.name} question"
            )
        return redirect("listcustom")
    else: form = CustomSubmissionForm()

    return render(request, "create_custom_question.html", {"courses": courses, 'form':form})



@user_approved_required
@login_required
def listCustomQuestions(request):
    customquestions = CustomQuestion.objects.order_by('course').all()
    return render(request, 'list_custom_questions.html', {
        'customquestions':customquestions
    })


@user_approved_required
@login_required
def customquestion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = CustomQuestion.objects.filter(course=course).first()

    if request.method == 'POST':
        print(request.POST)  # Debugging: Print POST data
        uploaded_images = request.FILES.getlist("images")  # Retrieve uploaded images
        form = CustomSubmissionForm(request.POST)

        if form.is_valid():  # Ensure the form is valid
            response = form.cleaned_data['response']
            question_id = request.POST.get('question_id')
            question = get_object_or_404(CustomQuestion, id=question_id)

            # Prevent staff submissions
            if hasattr(request.user, 'tutorial_center') or hasattr(request.user, 'tutor'):
                messages.success(request, f"{questions} have been successfully received. However, submissions are restricted for staff accounts.")
                return HttpResponseRedirect('/all_theories')

            # Create CustomGrade instance
            custom_grade = CustomQuestionResponse.objects.create(
                student=request.user,
                question=question,
                response=response,
                submission_id=uuid.uuid4()
            )

            # Initialize storage for image upload
            storage = SupabaseStorage()
            try:
                print("Uploading images...")
                for image in uploaded_images:
                    # Define storage path
                    storage_path = f"custom/{image.name}"
                    print(f"Uploading file: {image.name}")

                    # Save to Supabase and get URL
                    filename = storage.save(storage_path, image)
                    print("Uploaded")
                    image_url = storage.url(filename)
                    print(f'url : {image_url}')

                    # Save image record to UploadedImage model
                    UploadedImageCustom.objects.create(custom_grade=custom_grade, image=image_url)
                print("Images uploaded successfully.")
            except Exception as e:
                print(f"Error uploading images: {e}")
                messages.error(request, "Failed to upload one or more images. Please try again.")

            # Send email notification to tutor
            tutor = Tutor.objects.filter(speciality=course).first()
            if tutor and tutor.user.email:
                sender_email = 'princejetro123@gmail.com'
                sender_password = "iatu bier ypec yeqq"
                recipient_email = tutor.user.email
                subject = "New Theory Practice Submission"
                body = f"""
Dear {tutor.user.username},

A new theory practice response has been submitted by {request.user.get_full_name()} for the course '{course.name}'.

Please log in to your dashboard to review and grade the submission.

Best regards,
Tutorial Haven Tech Team
"""

                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(sender_email, sender_password)
                        smtp.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
                        print(f"Notification email sent to {tutor.user.email}.")
                except Exception as e:
                    print(f"Failed to send email to {tutor.user.email}: {e}")

            # Success message and redirect
            messages.success(request, f"{questions} Successfully Submitted! Your Tutor will grade and get back to you soon.")
            ActivityLog.objects.create(
            user=request.user,
            action=f"Practiced Custom questions for {course.name}"
            )
            return HttpResponseRedirect('/all_custom_questions')
        else:
            # Form validation error
            messages.error(request, "Answers Cannot Be Blank. You must submit an answer.")
    else:
        form = TheorySubmissionForm()

    context = {
        'course': course,
        'theory_questions': questions,
        'form': form,
    }
    return render(request, 'customquestions.html', context)


@user_approved_required
@login_required
def list_pending_custom_question(request):

    # Fetch all pending grades 
    pending_grades = CustomQuestionResponse.objects.filter(score=0)
    # Pass the data to the template
    context = {
        'pending_grades': pending_grades,
    }
    return render(request, 'pending_custom_grades.html', context)

@user_approved_required
@login_required
def grade_custom_questions(request, grade_id):
    # Fetch the TheoryGrade object
    question_grade = get_object_or_404(CustomQuestionResponse, id=grade_id)
    images = UploadedImageCustom.objects.filter(custom_grade=question_grade)  # Retrieve all related images

    # Ensure the user has the right to grade (e.g., is a tutor)
    if not hasattr(request.user, 'tutor') or not request.user.tutor:
        messages.error(request, "You do not have permission to grade this question.")
        return redirect('myprofile')  # Redirect to a suitable page

    # Handle form submission
    if request.method == 'POST':
        form = CustomGrade(request.POST, instance=question_grade)
        if form.is_valid():
            form.save()  # Save the updated score
            messages.success(request, "Score updated successfully!")
            return redirect('pending_custom_grades', tutor_id=request.user.tutor.id)  # Redirect to pending grades
    else:
        form = CustomGrade(instance=question_grade)

    # Pass data to the template
    context = {
        'theory_grade': question_grade,
        'form': form,
        'images': images,  # Pass all images to the template
    }
    ActivityLog.objects.create(
            user=request.user,
            action=f"Graded Custom Question for {question_grade.student.username} {question_grade.question.course.name}"
            )
    return render(request, 'grade_custom_questions.html', context)


@login_required
@user_approved_required
def listActivity(request):
    if hasattr(request.user, 'tutorial_center'):
        # If the user is a tutorial center, fetch activities of all students and tutors under them
        user_students = request.user.tutorial_center.students.all().values_list('user', flat=True)
        user_tutors = request.user.tutorial_center.tutors.all().values_list('user', flat=True)
        
        # Combine the lists of users
        user_list = list(user_students) + list(user_tutors)
        
        # Fetch activities for these users
        activities = ActivityLog.objects.filter(user__in=user_list).order_by('-timestamp')
    else:
        # If the user is a tutor or student, fetch only their own activities
        activities = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'activities': activities,
    }

    return render(request, 'activity_list.html', context)

openai.api_key = api_key

def ai_playground(request):
    """Main AI Playground page."""
    return render(request, "ai_playground.html")

def interactive_learning(request):
    """Interactive learning assistant."""
    if request.method == "POST":
        data = json.loads(request.body)
        student_query = data.get("query")
        feature = data.get("feature", "question_answering")

        try:
            response_content = None
            if feature == "question_answering":
                response_content = handle_question_answering(student_query)
            elif feature == "summarization":
                response_content = handle_summarization(student_query)
            elif feature == "explanation":
                response_content = handle_explanation(student_query)
            elif feature == "quiz":
                response_content = handle_quiz_generation(student_query)            
            return JsonResponse({"response": response_content})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"response": "An error occurred. Please try again."}, status=500)
    return JsonResponse({"response": "Invalid request method."}, status=400)

def handle_question_answering(query):
    """Real-time Q&A support."""
    return call_openai_api("You are a tutor. Provide a concise and accurate answer to the student's question.", query)

def handle_summarization(content):
    """Generate a summary of content."""
    return call_openai_api("You are a summarization expert. Summarize the following content:", content)

def handle_explanation(query):
    """Provide detailed explanations of concepts."""
    return call_openai_api("You are an educator. Provide a detailed explanation of the following concept:", query)

def handle_quiz_generation(content):
    """Generate quizzes or flashcards."""
    return call_openai_api("You are a quiz master. Generate an engaging 5-question quiz on the following topic:", content)


def call_openai_api(system_message, user_message):
    """Call the OpenAI API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]
    )
    return response.choices[0].message.content.replace("\n", "<br>").replace("---", "<hr>")
