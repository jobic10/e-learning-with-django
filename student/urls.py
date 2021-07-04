from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name="studentDashboard"),
    path('course/allocation', views.courseRegistration, name='courseRegistration')
]
