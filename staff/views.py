from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q, OuterRef, Exists
from .models import CourseAllocation
from e_learning.functions import get_session, validate_access, fetch_answer_to_this_assignment, format_date
from student.models import CourseRegistration
from classroom.models import *
from classroom.forms import *
from datetime import datetime
from django.http import JsonResponse
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


def staffClassroom(request, token):
    try:
        course_reg = validate_access(token, request, 'staff')
        # if course_id == False or course_id < 1 or not course_id:
        #     raise("Access Denied")
        session = get_session()
        # staff = request.user.staff
        # course_reg = CourseAllocation.objects.get(
        #     staff=staff, course_id=course_id, session=session, approved=True)
        assignments = Assignment.objects.filter(
            session=session, course=course_reg.course)
        posts = Stream.objects.all().order_by('-id')
        form = NewPostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                this_form = form.save(commit=False)
                this_form.user = request.user
                this_form.save()
                messages.success(request, "New Post Created")
                return redirect(reverse('staffClassroom', args=[token]))
            else:
                messages.error(request, "Form invalid")

        context = {
            'course': course_reg,
            'no_of_students': CourseRegistration.objects.filter(course=course_reg.course, approved=True, session=session).count(),
            'no_of_assignments': assignments.count(),
            'expired_assignments': assignments.filter(expiry_date__lt=datetime.today()).count(),
            'active_assignments': assignments.filter(expiry_date__gt=datetime.today()).count(),
            'posts': posts,
            'form': form
        }
        return render(request, path("classroom_dashboard"), context)
    except Exception as e:
        print(e, "Here ---<")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('staffDashboard'))


def get_assignment_form(request, token):
    try:
        course_reg = validate_access(token, request, 'staff')
        staff = request.user.staff
        assignment_form = AssignmentForm(request.POST or None)
        context = {
            'course': course_reg,
            'form': assignment_form
        }

        if request.method == 'POST':
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.course = course_reg.course
                assignment.session = get_session()
                assignment.save()
                context['form'] = AssignmentForm()
                messages.success(request, "New Assignment Created")
            else:
                messages.error(request, "Please fill form properly")
        return render(request, path("classroom_assignment"), context)
    except Exception as e:
        print(e, "Here ---<")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('staffDashboard'))


def view_all_assignments(request, token):
    course_reg = validate_access(token, request, 'staff')
    try:
        assignments = Assignment.objects.filter(
            session=get_session(), course=course_reg.course).order_by('-expiry_date')
        context = {
            'assignments': assignments,
            'course': course_reg
        }
        return render(request, path("classroom_view_assignment"), context)
    except Exception as e:
        print(e, "Here --- <")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('staffDashboard'))


def edit_assignment_form(request, token, assignment_id):
    try:
        course_reg = validate_access(token, request, 'staff')
        assignment = Assignment.objects.get(
            id=assignment_id, course=course_reg.course, session=get_session())
        form = AssignmentForm(request.POST or None, instance=assignment)
        context = {
            'form': form,
            'course': course_reg
        }
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Assignment Updated")
            else:
                messages.error(request, "Form invalid")

        return render(request, path("edit_assignment_form"), context)
    except Exception as e:
        print(e, "Here --- <")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('staffDashboard'))


def view_submission(request, token, assignment_id):
    try:
        course_reg = validate_access(token, request, 'staff')
        assignment = Assignment.objects.get(
            id=assignment_id, course=course_reg.course, session=get_session())
        submissions = Submission.objects.filter(assignment=assignment)
        context = {
            'submissions': submissions,
            'course': course_reg,
            'assignment_name': assignment.title
        }
        return render(request, path("classroom_view_assignment_submission"), context)
    except Exception as e:
        print(e, "Here --- <")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('staffDashboard'))


def get_student_answer(request, token, submission_id):
    context = {
        'error': False
    }
    try:
        course_reg = validate_access(token, request, 'staff')
        submission = Submission.objects.get(
            id=submission_id, assignment__course=course_reg.course)
        error, value = fetch_answer_to_this_assignment(
            submission.student, submission.assignment.id)
        if not error:
            context['submitted_date'] = format_date(value.submission_date)
            context['answer'] = value.answer
        context['error'] = error
    except Exception as e:
        print(e, "Here ---<")
        context['error'] = True
    return JsonResponse(context, safe=True)
