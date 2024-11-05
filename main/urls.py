from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_student, name='register'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('login/', views.loginview, name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout URL
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<str:department_name>/courses/', views.list_courses, name='list_courses'),
    path('courses/', views.list_all_courses, name='course'),
    path('courses/<str:course_name>/', views.course_detail, name='course_detail'),
    path('courses/<str:topic_name>/topic', views.topic_detail, name='topic_detail'),
]
