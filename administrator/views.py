from django.shortcuts import render, reverse, redirect
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
# Administrative Functions


def path(html_file):
    return f"administrator/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


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


def delete_department(request, id):
    try:
        # ! Later, check to see students who are enrolled to this department before deleting
        department = Department.objects.get(id=id)
        department.delete()
        messages.success(request, "Department deleted")
    except:
        messages.error(request, "Access Denied")
    return redirect(reverse('add_department'))


def fetch_department_by_id(request, id):
    context = {
        'error': False
    }
    try:
        department = Department.objects.get(id=id)
        form = AddDepartmentForm(request.POST or None, instance=department)
        context['form'] = form.as_p()
    except:
        context['error'] = True
    return JsonResponse(context)


def updateDepartment(request):
    try:
        department = Department.objects.get(id=request.POST.get('dept_id'))
        form = AddDepartmentForm(request.POST or None, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('add_department'))

# Start of Course


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


def delete_course(request, id):
    try:
        # ! Later, check to see students who are enrolled to this course before deleting
        course = Course.objects.get(id=id)
        course.delete()
        messages.success(request, "Course deleted")
    except:
        messages.error(request, "Access Denied")
    return redirect(reverse('add_course'))


def fetch_course_by_id(request, id):
    context = {
        'error': False
    }
    try:
        course = Course.objects.get(id=id)
        form = AddCourseForm(request.POST or None, instance=course)
        context['form'] = form.as_p()
    except:
        context['error'] = True
    return JsonResponse(context)


def updateCourse(request):
    try:
        course = Course.objects.get(id=request.POST.get('course_id'))
        form = AddCourseForm(request.POST or None, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('add_course'))

# Start of Session


def add_session(request):
    form = AddSessionForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Session Added")
            context['form'] = AddSessionForm()
        else:
            messages.error(request, "Invalid Data Provided")
    context['sessions'] = Session.objects.all()

    return render(request, path('session'), context)


def delete_session(request, id):
    try:
        # ! Later, check to see students who are enrolled to this session before deleting
        session = Session.objects.get(id=id)
        session.delete()
        messages.success(request, "Session deleted")
    except:
        messages.error(request, "Access Denied")
    return redirect(reverse('add_session'))


def fetch_session_by_id(request, id):
    context = {
        'error': False
    }
    try:
        session = Session.objects.get(id=id)
        form = AddSessionForm(request.POST or None, instance=session)
        context['form'] = form.as_p()
    except:
        context['error'] = True
    return JsonResponse(context)


def updateSession(request):
    try:
        session = Course.objects.get(id=request.POST.get('session_id'))
        form = AddSessionForm(request.POST or None, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('add_session'))
