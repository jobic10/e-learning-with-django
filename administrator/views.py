from django.shortcuts import render, reverse, redirect
from .forms import *
from account.forms import CustomUserForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
# Administrative Functions


def path(html_file):
    return f"administrator/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def manageDepartment(request):
    form = AddDepartmentForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added")
            context['form'] = AddDepartmentForm()
            return redirect(reverse('manageDepartment'))
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
    return redirect(reverse('manageDepartment'))


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

    return redirect(reverse('manageDepartment'))

# Start of Course


def manageCourse(request):
    form = AddCourseForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Course Added")
            context['form'] = AddCourseForm()
            return redirect(reverse('manageCourse'))

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
    return redirect(reverse('manageCourse'))


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

    return redirect(reverse('manageCourse'))

# Start of Session


def manageSession(request):
    form = AddSessionForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Session Added")
            context['form'] = AddSessionForm()
            return redirect(reverse('manageSession'))

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
    return redirect(reverse('manageSession'))


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
        session = Session.objects.get(id=request.POST.get('session_id'))
        form = AddSessionForm(request.POST or None, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('manageSession'))

# Start of Student


def manageStudent(request):
    form = CustomUserForm(request.POST or None)
    form2 = AddStudentForm(request.POST or None)
    context = {
        'form': form,
        'form2': form2
    }
    if request.method == 'POST':
        if form.is_valid() and form2.is_valid():
            admin = form.save(commit=False)
            student = form2.save(commit=False)
            student.admin = admin
            admin.save()
            student.save()
            messages.success(request, "Student Added")
            context['form'] = AddStudentForm()
            return redirect(reverse('manageStudent'))

        else:
            messages.error(request, "Invalid Data Provided")
    paginator = Paginator(Student.objects.all(), 50)
    page = request.GET.get('page', 1)
    context['students'] = paginator.get_page(page)

    return render(request, path('student'), context)


def delete_student(request, id):
    try:
        # ! Later, check associated data with this student
        student = Student.objects.get(id=id)
        student.delete()
        messages.success(request, "Student deleted")
    except:
        messages.error(request, "Access Denied")
    return redirect(reverse('manageStudent'))


def fetch_student_by_id(request, id):
    context = {
        'error': False
    }
    try:
        student = Student.objects.get(id=id)
        form = AddStudentForm(request.POST or None, instance=student)
        context['form'] = form.as_p()
    except:
        context['error'] = True
    return JsonResponse(context)


def updateStudent(request):
    try:
        student = Student.objects.get(id=request.POST.get('student_id'))
        form = AddStudentForm(request.POST or None, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('manageStudent'))

# Start of Staff


def manageStaff(request):
    form = AddStaffForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Staff Added")
            context['form'] = AddStaffForm()
        else:
            messages.error(request, "Invalid Data Provided")
    context['staffs'] = Staff.objects.all()

    return render(request, path('staff'), context)


def delete_staff(request, id):
    try:
        # ! Later, check associated data with this staff
        staff = Staff.objects.get(id=id)
        staff.delete()
        messages.success(request, "Staff deleted")
    except:
        messages.error(request, "Access Denied")
    return redirect(reverse('manageStaff'))


def fetch_staff_by_id(request, id):
    context = {
        'error': False
    }
    try:
        staff = Staff.objects.get(id=id)
        form = AddStaffForm(request.POST or None, instance=staff)
        context['form'] = form.as_p()
    except:
        context['error'] = True
    return JsonResponse(context)


def updateStaff(request):
    try:
        staff = Staff.objects.get(id=request.POST.get('staff_id'))
        form = AddStaffForm(request.POST or None, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
        else:
            messages.error(request, "Access Denied")
    except:
        messages.error(request, "Access Denied!")

    return redirect(reverse('manageStaff'))
