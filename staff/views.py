from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q
from .models import CourseAllocation
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
    this_session = SESSION(request)['ACADEMIC_SESSION']
    courses = Course.objects.filter(
        Q(department__is_general=True) | Q(department=my_department),)
    my_courses = CourseAllocation.objects.filter(
        staff=staff, approved=True, session=this_session)
    is_registered = CourseAllocation.objects.filter(
        session=this_session, staff=staff, approved=True).exists()
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
                if not CourseAllocation.objects.filter(staff=staff, course=this_course, session=this_session).exists():
                    CourseAllocation(
                        staff=staff, course=this_course, session=this_session).save()
                insert += 1
        except Exception as e:
            print(e)
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
        return redirect(reverse('courseAllocation'))

    return render(request, path("course_allocation"), context)
