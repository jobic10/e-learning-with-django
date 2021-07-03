from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q
from e_learning.context_processors import SESSION
# Create your views here.


def path(html_file):
    return f"staff/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def courseAllocation(request):
    staff = request.user.staff
    my_department = staff.department
    courses = Course.objects.filter(
        Q(department__is_general=True) | Q(department=my_department),)
    context = {
        'courses': courses,
    }
    if request.method == 'POST':
        pass
    return render(request, path("course_allocation"), context)
