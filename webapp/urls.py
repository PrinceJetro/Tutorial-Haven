from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register_institution/', views.register_owner, name='register_institution'),
    path('register_tutor/', views.register_tutor, name='register_tutor'),
    path('register_student/', views.register_student, name='register_student'),
    path('approve-users/', views.approve_users, name='approve_users'),
    path('<str:tutorial>/students', views.list_tutorial_students, name='list_tutorial_students'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('login/', views.loginview, name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout URL
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<int:department_id>/courses/', views.list_courses, name='list_courses'),
    path('courses/', views.list_all_courses, name='course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:topic_id>/topic', views.topic_detail, name='topic_detail'),
    path('pastquestions/<int:course_id>/', views.pastquestion, name='pastquestions'),
    path('pastquestions/<int:pastpq_id>/keypoints', views.key_points, name='keypoints'),
]
