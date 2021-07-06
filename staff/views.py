from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q, OuterRef, Exists
from .models import CourseAllocation
from e_learning.functions import get_session
from student.models import CourseRegistration

# Create your views here.


def path(html_file):
    return f"staff/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def courseAllocation(request):
    staff = request.user.staff
    my_department = staff.department
    this_session = get_session()
    courses = Course.objects.filter(~Exists(CourseAllocation.objects.filter(
        approved=True, course=OuterRef('courseallocation__course'), session=this_session)), Q(department__is_general=True) | Q(department=my_department))
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
                # Check if this course is available for the staff
                if this_course.department != my_department and not this_course.department.is_general:
                    messages.error(
                        request, "Sorry, this course is not available for you")
                    return redirect(reverse('courseAllocation'))

                if CourseAllocation.objects.filter(course=this_course, session=this_session, approved=True).exists():
                    messages.error(request, "Sorry, " + str(this_course) +
                                   " has already been approved for a lecturer")
                    return redirect(reverse('courseAllocation'))

                if not CourseAllocation.objects.filter(staff=staff, course=this_course, session=this_session).exists():
                    CourseAllocation(
                        staff=staff, course=this_course, session=this_session).save()
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
        return redirect(reverse('courseAllocation'))

    return render(request, path("course_allocation"), context)


def courseStatus(request):
    staff = request.user.staff
    this_session = get_session()
    my_department = staff.department
    my_courses = CourseAllocation.objects.filter(
        staff=staff, approved=True, session=this_session)
    courses = CourseRegistration.objects.filter(
        course__in=my_courses.values_list('course_id'), approved=None, session=this_session)
    context = {
        'courses': courses
    }
    return render(request, path("course_status"), context)


def courseAppResponse(request, this_id, status):
    staff = request.user.staff
    my_department = staff.department
    if status != 'approved' and status != 'rejected':
        messages.error(request, "Access Denied")
    else:
        try:
            course_reg = CourseRegistration.objects.get(id=this_id)
            this_session = get_session()
            CourseAllocation.objects.get(
                staff=staff, course_id=course_reg.course_id, approved=True, session=this_session)
            return None
            if status == 'rejected':
                course_reg.delete()
            else:
                course_reg.approved = True
                course_reg.save()
            messages.success(
                request, "Action completed. Course " + str(status))

        except Exception as e:
            messages.error(request, "You do not have access to this resource")
    return redirect(reverse('courseStatus'))
