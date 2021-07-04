from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q, OuterRef, Exists
from e_learning.functions import get_session
from .models import CourseRegistration

# Create your views here.


def path(html_file):
    return f"student/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def courseRegistration(request):
    student = request.user.student
    my_department = student.department
    this_session = get_session()
    courses = Course.objects.filter(~Exists(CourseRegistration.objects.filter(
        approved=True, course=OuterRef('courseregistration__course'), session=this_session)), Q(department__is_general=True) | Q(department=my_department))
    my_courses = CourseRegistration.objects.filter(
        student=student, approved=True, session=this_session)
    is_registered = CourseRegistration.objects.filter(
        session=this_session, student=student, approved=True).exists()
    context = {
        'courses': courses,
        'selected_courses': my_courses,
        'registered': is_registered
    }
    if request.method == 'POST':
        pass
        return redirect(reverse('courseRegistration'))

    return render(request, path("course_reg"), context)
