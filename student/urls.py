from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="studentDashboard"),
    path('course/allocation', views.courseRegistration, name='courseRegistration'),
    path('classroom/<token>/', views.studentClassroom, name='studentClassroom'),
    path('classroom/<token>/assignments/',
         views.active_assignments, name='studentActiveAssignments'),
    path('classroom/<token>/assignments/<int:assignment_id>/submit',
         views.submit_assignment, name='studentSubmitAssignments'),
    path('classroom/<token>/assignment/<int:assignment_id>/answer',
         views.get_answer, name='get_answer'),
    path("classroom/<token>/stream/all/<int:stream_id>",
         views.student_view_post, name='student_view_post'),
]
