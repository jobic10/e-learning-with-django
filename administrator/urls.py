from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="adminDashboard"),
    path('course/add', views.add_course, name="add_course"),
    path('department/add', views.add_department, name="add_department"),
    path('department/delete/<int:id>',
         views.delete_department, name="delete_department"),
    path('department/get/<int:id>', views.fetch_department_by_id,
         name='fetch_department_by_id'),
    path('department/update', views.updateDepartment, name='updateDepartment'),

    #     Start of Course
    path('course/delete/<int:id>',
         views.delete_course, name="delete_course"),
    path('course/get/<int:id>', views.fetch_course_by_id,
         name='fetch_course_by_id'),
    path('course/update', views.updateCourse, name='updateCourse'),
]
