# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import  Student, Course, Department, Topic, TutorialCenter, PastQuestionsObj, KeyPoints, Tutor, PastQuestionsTheory, ObjGrade,TheoryGrade, UserCourseProgress
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.db.models import Avg
from webapp.storage import SupabaseStorage
from .forms import TheorySubmissionForm, GradeForm
import smtplib
import ssl
from django.db.models import Avg  # Import Avg for aggregation
import uuid  # Ensure you have imported this at the top of the file
from django.contrib import messages  # Import messages for feedback to users






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


@login_required
def list_departments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "cool/departments.html", {"departments": departments})


@login_required
def list_all_courses(request):
    all_courses = Course.objects.order_by('name').all()
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
    topics = course.topics.all()  # Order related topics alphabetically by 'name'
    userprogress = UserCourseProgress.objects.filter(user=request.user, course=course).first()

    return render(
        request, 
        'course_detail.html', 
        {'course': course, 'topics': topics, 'userprogress': userprogress}
    )

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
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


@login_required
def cbtquestion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = PastQuestionsObj.objects.filter(course=course)

    if request.method == 'POST':
        if hasattr(request.user, 'tutorial_center') or hasattr(request.user, 'tutor'):
            messages.success(request, "Practice session has been successfully received. However, submissions are restricted for staff accounts.")
            return HttpResponseRedirect('/allcourses/')
        score = 0
        total_questions = questions.count()
        submission_id = uuid.uuid4()  # Generate a unique submission ID for this attempt

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

            # Save individual grade for this question
            ObjGrade.objects.create(
                user=request.user,
                question=question,
                course=course,
                score=100 if selected_option == question.correct_option else 0,
                submission_id=submission_id,  # Assign the unique submission ID
            )

        # Calculate overall percentage score for this attempt
        percentage_score = (score / total_questions) * 100

        # Update or create the user's progress for this course
        user_progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
        )
        user_progress.attempts += 1
        # Update the average percentage considering all attempts
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
            'total_percent': user_progress.percentage
        }
        return render(request, 'cbt_result.html', context)

    context = {
        'course': course,
        'cbt_questions': questions,
    }
    return render(request, 'pastquestion.html', context)

@login_required
def listTheory(request):
    theories = PastQuestionsTheory.objects.all()
    return render(request, 'list_theory.html', {
        'theories':theories
    })


@login_required
def theoryquestion(request, course_id, year):
    course = get_object_or_404(Course, id=course_id)
    print(course)
    questions = PastQuestionsTheory.objects.filter(course=course, year=year).first()
    print(questions)
    
    if request.method == 'POST':
        
        form = TheorySubmissionForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            question_id = request.POST.get('question_id')  # ID of the question being answered
            print(request.POST)
            print(f"here is the  question id {question_id}")

            question = get_object_or_404(PastQuestionsTheory, id=question_id)
            if hasattr(request.user, 'tutorial_center') or hasattr(request.user, 'tutor'):
                messages.success(request,f"{questions} have been successfully received. However, submissions are restricted for staff accounts.")
                return HttpResponseRedirect('/all_theories') 

            submission = TheoryGrade.objects.create(
                user=request.user,
                question=question,
                question_text = question.question_text,
                course=course,
                response=response,
                submission_id=uuid.uuid4()
            )
             # Fetch the tutor for the course
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



            messages.success(request, F"{questions} Successfully Submitted! Your Tutor will grade and get back to you soon.")
            return HttpResponseRedirect('/all_theories') 
        else:
            messages.error(request, f"Answers Cannot Be Blank, you must submit an answer" )
    else:
        form = TheorySubmissionForm()

    context = {
        'course': course,
        'theory_questions': questions,
        'form': form,
    }
    return render(request, 'theoryquestion.html', context)

@login_required
def list_pending_theory(request, tutor_id):
    # Get the logged-in tutor
    tutor = get_object_or_404(Tutor, user=request.user)

    # Get all the tutor's specialities (courses)
    speciality_courses = tutor.speciality.all()
    print(speciality_courses)

    # Fetch all pending grades for the tutor's courses
    pending_grades = TheoryGrade.objects.filter(course_id__in=speciality_courses, score=0)
    print(pending_grades)

    # Pass the data to the template
    context = {
        'pending_grades': pending_grades,
        'courses': speciality_courses,  # Pass all courses for the tutor
    }
    return render(request, 'pending_grades.html', context)

@login_required
def grade_theory(request, grade_id):
    # Fetch the TheoryGrade object
    theory_grade = get_object_or_404(TheoryGrade, id=grade_id)
    
    # Ensure the user has the right to grade (e.g., is a tutor)
    if not request.user.is_authenticated or not hasattr(request.user, 'tutor') or not request.user.tutor:
        messages.error(request, "You do not have permission to grade this question.")
        return redirect('myprofile')  # Redirect to a suitable page

    
    # Handle form submission
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=theory_grade)
        if form.is_valid():
            form.save()  # Save the updated score
            messages.success(request, "Score updated successfully!")
            return redirect('myprofile')  # Redirect to a suitable page
    else:
        form = GradeForm(instance=theory_grade)

    # Pass data to the template
    context = {
        'theory_grade': theory_grade,
        'form': form,
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



@login_required
def myreport(request):
    objgrades = UserCourseProgress.objects.filter(user=request.user).order_by('-percentage')
    theorygrades = TheoryGrade.objects.filter(user=request.user).order_by('-score')

    print(theorygrades)
    graded_data = []
    graded_data_theory = []

    for grade in objgrades:
        credits = calculate_credits(grade.percentage)
        graded_data.append({
            "course": grade.course.name,
            "percentage": grade.percentage,
            "credits": credits,
            "attempts": grade.attempts
        })
    for grade in theorygrades:
        print(grade)
        credits = calculate_credits(grade.score)
        graded_data_theory.append({
            "course": grade.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "year": grade.question.year
        })

    context = {
        "graded_data": graded_data,
        "graded_data_theory": graded_data_theory,
    }
    return render(request, 'report.html', context)


@login_required
def studentsreport(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    objgrades = UserCourseProgress.objects.filter(user=student.user).order_by('-percentage')
    theorygrades = TheoryGrade.objects.filter(user=student.user).order_by('-score')

    print(theorygrades)
    graded_data = []
    graded_data_theory = []

    for grade in objgrades:
        credits = calculate_credits(grade.percentage)
        graded_data.append({
            "course": grade.course.name,
            "percentage": grade.percentage,
            "credits": credits,
            "attempts": grade.attempts
        })
    for grade in theorygrades:
        print(grade)
        credits = calculate_credits(grade.score)
        graded_data_theory.append({
            "course": grade.course.name,
            "percentage": grade.score,
            "credits": credits,
            "note": grade.note,
            "submitted_at": grade.submitted_at,
            "year": grade.question.year
        })

    context = {
        "graded_data": graded_data,
        "graded_data_theory": graded_data_theory,
        "student":student
    }
    return render(request, 'studentsreport.html', context)





@login_required
def key_points(request, pastpq_id):
    pastpq = get_object_or_404(PastQuestionsObj, id=pastpq_id)
    keypoint = KeyPoints.objects.filter(past_question=pastpq).first()  # Use .first() to fetch the single object

    return render(request, 'cool/keypoints.html', {'keypoint': keypoint})