from django.urls import path
from . import views
from classroom import student_views


urlpatterns = [
    path('', views.dashboard, name="studentDashboard"),
    path('course/allocation', views.courseRegistration, name='courseRegistration'),
    path('classroom/<token>/', views.studentClassroom, name='studentClassroom'),
]
