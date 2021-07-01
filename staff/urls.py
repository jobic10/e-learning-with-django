from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="staffDashboard"),
    path('course/allocation', views.courseAllocation, name="courseAllocation"),

]
