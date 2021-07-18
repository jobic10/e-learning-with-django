from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="staffDashboard"),
    path('course/allocation', views.courseAllocation, name="courseAllocation"),
    path('course/reg/status', views.courseStatus, name="courseStatus"),
    path('course/application/response/<int:this_id>/<str:status>',
         views.courseAppResponse, name='courseAppResponse'),
    path('classroom/<token>/', views.staffClassroom, name='staffClassroom'),
    path('classroom/<str:token>/new_assignment',
         views.get_assignment_form, name='get_assignment_form'),
    path('classroom/<str:token>/assignments/',
         views.view_all_assignments, name='view_all_assignments'),
    path('classroom/<str:token>/assignment/edit/<int:assignment_id>',
         views.edit_assignment_form, name="edit_assignment_form"),
    path('classroom/<str:token>/assignment/submission/<int:assignment_id>',
         views.view_submission, name="view_submission"),
    path("classroom/<str:token>/assignment/answer/<int:submission_id>",
         views.get_student_answer, name='get_student_answer'),


]
