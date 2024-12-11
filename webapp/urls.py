from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register_institution/', views.register_owner, name='register_institution'),
    path('register_tutor/', views.register_tutor, name='register_tutor'),
    path('register_student/', views.register_student, name='register_student'),
    path('approve-users/', views.approve_users, name='approve_users'),
    path('<int:tutorial_id>/students', views.list_tutorial_students, name='list_tutorial_students'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('login/', views.loginview, name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout URL
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<int:department_id>/courses/', views.list_courses, name='list_courses'),
    path('allcourses/', views.list_all_courses, name='allcourses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:topic_id>/topic', views.topic_detail, name='topic_detail'),
    path('pastquestions/<int:course_id>/', views.cbtquestion, name='pastquestions'),
    path('pastquestions/<int:course_id>/<int:year>/theory', views.theoryquestion, name='theory'),
    path('grade/theory/<int:grade_id>/', views.grade_theory, name='grade_theory'),
    path('pending_gradings/<int:tutor_id>/', views.list_pending_theory, name='pending_gradings'),
    path("all_theories", views.listTheory, name="listTheory"),
    path('pastquestions/<int:pastpq_id>/keypoints', views.key_points, name='keypoints'),
    path('myreport/', views.myreport, name='myreport'),
    path('studentsreport/<int:student_id>', views.studentsreport, name='studentsreport'),
    path('search/', views.search, name='search'),  # Add search route

]
