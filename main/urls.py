from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/owner/', views.register_owner, name='register_owner'),
    path('register/tutor/', views.register_tutor, name='register_tutor'),
    path('register/student/', views.register_student, name='register_student'),
    path('profile/<str:name>', views.profile, name='profile'),
    path('approve-users/', views.approve_users, name='approve_users'),
    path('login/', views.loginview, name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout URL
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<str:department_name>/courses/', views.list_courses, name='list_courses'),
    path('courses/', views.list_all_courses, name='course'),
    path('courses/<str:course_name>/', views.course_detail, name='course_detail'),
    path('courses/<str:topic_name>/topic', views.topic_detail, name='topic_detail'),
    path('<str:tutorial>', views.about_tutorial, name='about_tutorial'),
    path('<str:tutorial>/students', views.list_tutorial_students, name='list_tutorial_students'),
]
