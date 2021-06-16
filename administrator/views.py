from django.shortcuts import render
from .forms import *
from django.contrib import messages
# Administrative Functions


def path(html_file):
    return f"administrator/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def add_course(request):
    form = AddCourseForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Course Added")
            context['form'] = AddCourseForm()
        else:
            messages.error(request, "Invalid Data Provided")
    context['courses'] = Course.objects.all()

    return render(request, path('course'), context)


def add_department(request):
    form = AddDepartmentForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added")
            context['form'] = AddDepartmentForm()
        else:
            messages.error(request, "Invalid Data Provided")
    context['departments'] = Department.objects.all()
    return render(request, path('department'), context)
