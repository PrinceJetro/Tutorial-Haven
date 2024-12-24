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
    path('customquestion/<int:course_id>/question', views.customquestion, name='custom_questions'),
    path('create_custom_question/', views.create_custom_question, name='create_custom_question'),
    path('grade/customquestion/<int:grade_id>/', views.grade_custom_questions, name='grade_custom'),
    path('pending_custom_gradings/', views.list_pending_custom_question, name='pending_custom_grades'),
    path("all_theories", views.listTheory, name="listTheory"),
    path("all_custom_questions", views.listCustomQuestions, name="listcustom"),
    path('pastquestions/<int:pastpq_id>/keypoints', views.key_points, name='keypoints'),
    path('myreport/', views.myreport, name='myreport'),
    path('studentsreport/<int:student_id>', views.studentsreport, name='studentsreport'),
    path('deletestudent/<int:student_id>', views.delete_student, name='deletestudent'),
    path('search/', views.search, name='search'),  # Add search route
    path("achievements/", views.achievements_list, name="achievements_list"),
    path("progress/", views.user_progress, name="user_progress"),
    path("complete_topic/", views.complete_topic, name="complete_topic"),
    path("forums/", views.forum_list, name="forum_list"),
    path("forums/<int:forum_id>/", views.forum_detail, name="forum_detail"),
    path("forums/create/", views.create_forum, name="create_forum"),
    path("forums/delete/<int:forum_id>", views.delete_forum, name="delete_forum"),
    path("activities", views.listActivity, name="activities"),
]
