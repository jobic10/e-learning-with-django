from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="staffDashboard"),
    path('course/allocation', views.courseAllocation, name="courseAllocation"),
    path('course/reg/status', views.courseStatus, name="courseStatus"),
    path('course/application/response/<int:this_id>/<str:status>',
         views.courseAppResponse, name='courseAppResponse'),
    path('classroom/<token>/', views.staffClassroom, name='staffClassroom'),

]
