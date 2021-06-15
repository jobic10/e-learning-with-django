from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="adminDashboard"),
    path('course/add', views.add_course, name="add_course"),
]
