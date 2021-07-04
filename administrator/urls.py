from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="adminDashboard"),
    #     Start of Department
    path('department/add', views.manageDepartment, name="manageDepartment"),
    path('department/delete/<int:id>',
         views.delete_department, name="delete_department"),
    path('department/get/<int:id>', views.fetch_department_by_id,
         name='fetch_department_by_id'),
    path('department/update', views.updateDepartment, name='updateDepartment'),

    #     Start of Course
    path('course/add', views.manageCourse, name="manageCourse"),
    path('course/delete/<int:id>',
         views.delete_course, name="delete_course"),
    path('course/get/<int:id>', views.fetch_course_by_id,
         name='fetch_course_by_id'),
    path('course/update', views.updateCourse, name='updateCourse'),

    # Start of Session
    path('session/add', views.manageSession, name="manageSession"),
    path('session/delete/<int:id>',
         views.delete_session, name="delete_session"),
    path('session/get/<int:id>', views.fetch_session_by_id,
         name='fetch_session_by_id'),
    path('session/update', views.updateSession, name='updateSession'),

    #     Start of Staff
    path('staff/add', views.manageStaff, name="manageStaff"),
    path('staff/delete/<int:id>',
         views.delete_staff, name="delete_staff"),
    path('staff/get/<int:id>', views.fetch_staff_by_id,
         name='fetch_staff_by_id'),
    path('staff/update', views.updateStaff, name='updateStaff'),
    path('staff/course/allocation', views.viewCourseAllocations,
         name='viewCourseAllocations'),
    path('course/staff/allocation/response/<int:this_id>/<str:response>',
         views.approve_reject_course_allocation, name='responseCourseAllocation'),

    #     Start of Student
    path('student/add', views.manageStudent, name="manageStudent"),
    path('student/delete/<int:id>',
         views.delete_student, name="delete_student"),
    path('student/get/<int:id>', views.fetch_student_by_id,
         name='fetch_student_by_id'),
    path('student/update', views.updateStudent, name='updateStudent'),

    #     Start of Settings
    path('site/settings/', views.siteSettings, name='siteSettings'),

]
