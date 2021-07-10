from django.urls import path
# from . import student_views, staff_views, views
from staff import views as v
urlpatterns = [
    path('/idontevenknow/', v.courseAllocation, name="wahala"),
]
