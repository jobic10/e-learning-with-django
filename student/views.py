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
        course=OuterRef('courseregistration__course'), session=this_session, student=student)), Q(department__is_general=True) | Q(department=my_department))
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
        submitted_courses = request.POST.getlist('courses[]')
        course_id_length = len(submitted_courses)
        insert = 0
        if course_id_length < 1:
            messages.error(request, "Please select at least one course")
            return redirect(reverse('courseAllocation'))
        try:
            for course_id in submitted_courses:
                this_id = int(course_id)
                this_course = Course.objects.get(id=this_id)
                if this_course.department != my_department and not this_course.department.is_general:
                    messages.error(
                        request, "Sorry, this course is not available for you")
                    return redirect(reverse('courseAllocation'))
                if not CourseRegistration.objects.filter(student=student, course=this_course, session=this_session).exists():
                    CourseRegistration(
                        student=student, course=this_course, session=this_session).save()
                insert += 1
        except Exception as e:
            messages.error(
                request, "Please select appropriate course(s) " + str(e))
            return redirect(reverse('courseAllocation'))
        if insert == course_id_length:
            messages.success(request, "All selected courses have been saved")
        elif insert > 0:
            messages.info(request, "Some of your selected courses were saved")
        else:
            messages.error(
                request, "Error occurred while trying to save your data")
        return redirect(reverse('courseRegistration'))

    return render(request, path("course_reg"), context)
