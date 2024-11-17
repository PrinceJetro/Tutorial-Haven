from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register_institution/', views.register_institution, name='register_institution'),
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    path('register_student/', views.register_student, name='register_student'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('login/', views.loginview, name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout URL
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<int:department_id>/courses/', views.list_courses, name='list_courses'),
    path('courses/', views.list_all_courses, name='course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:topic_id>/topic', views.topic_detail, name='topic_detail'),
    path('cbt/<int:course_id>/', views.cbt_view, name='cbt'),
    path('allpastquestions', views.all_past_questions, name='allpastquestions'),
    path('pastquestions/<int:pastpq_id>/', views.past_questions, name='pastquestions'),
    path('pastquestions/<int:pastpq_id>/keypoints', views.key_points, name='keypoints'),
]
