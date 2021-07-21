from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q, OuterRef, Exists
from e_learning.functions import get_session, validate_access, fetch_answer_to_this_assignment, format_date
from .models import CourseRegistration
from classroom.models import *
from datetime import datetime
from classroom.forms import *
from django.http import JsonResponse
# Create your views here.


def path(html_file):
    return f"student/{html_file}.html"


def dashboard(request):
    session = get_session()
    student = request.user.student
    my_courses = CourseRegistration.objects.filter(
        student=student, session=session, approved=True)
    assignments = Assignment.objects.filter(
        session=session, course__in=my_courses.values_list('course_id'))
    context = {
        'all_assignments': assignments.count(),
        'active_assignments': assignments.filter(expiry_date__gt=datetime.today()).count(),
        'my_courses': my_courses.count()
    }
    return render(request, path("home"), context)


def courseRegistration(request):
    student = request.user.student
    my_department = student.department
    this_session = get_session()
    courses = Course.objects.filter(~Exists(CourseRegistration.objects.filter(
        course=OuterRef('courseregistration__course'), session=this_session, student=student)), Q(department__is_general=True) | Q(department=my_department)).distinct()
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


def studentClassroom(request, token):
    try:
        course_reg = validate_access(token, request, 'student')
        session = get_session()
        student = request.user.student
        assignments = Assignment.objects.filter(
            session=session, course=course_reg.course)
        posts = Stream.objects.filter(
            session=session, course=course_reg.course).order_by('-id')
        form = NewPostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                this_form = form.save(commit=False)
                this_form.user = request.user
                this_form.course = course_reg.course
                this_form.session = session
                this_form.save()
                messages.success(request, "New Post Created")
                return redirect(reverse('studentClassroom', args=[token]))
            else:
                messages.error(request, "Form invalid")
        context = {
            'course': course_reg,
            'no_of_students': CourseRegistration.objects.filter(course=course_reg.course, approved=True, session=session).count(),
            'no_of_assignments': assignments.count(),
            'expired_assignments': assignments.filter(expiry_date__lt=datetime.today()).count(),
            'active_assignments': assignments.filter(expiry_date__gt=datetime.today()).count(),
            'my_submission': Submission.objects.filter(student=student, assignment__session=session).count(),
            'posts': posts,
            'form': form

        }
        return render(request, path("classroom_dashboard"), context)
    except Exception as e:
        print(e, "Here ---<")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('studentDashboard'))


def active_assignments(request, token):
    try:
        session = get_session()
        course_reg = validate_access(token, request, 'student')
        assignments = Assignment.objects.filter(
            session=session, course=course_reg.course).order_by('-expiry_date')
        context = {
            'assignments': assignments,
            'course': course_reg
        }
        return render(request, path("classroom_all_assignment"), context)
    except Exception as e:
        print(e, "Here ---<")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('studentDashboard'))


def submit_assignment(request, token, assignment_id):
    try:
        session = get_session()
        course_reg = validate_access(token, request, 'student')
        assignment = Assignment.objects.get(
            session=session, course=course_reg.course, id=assignment_id)
        # Check if this assignment has expire
        if datetime.today().date() > assignment.expiry_date:
            messages.error(
                request, "You are trying to submit an assignment that has already pass the submission date")
            return redirect(reverse('studentDashboard'))
        form = SubmissionForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = request.user.student
                submission.save()
                messages.success(request, "Assignment submitted")
                return redirect(reverse('studentActiveAssignments', args=[token]))
        context = {
            'form': form,
            'course': course_reg,
            'assignment': assignment
        }
        return render(request, path("classroom_submit_assignment"), context)
    except Exception as e:
        print(e, "Here ---<")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('studentDashboard'))


def get_answer(request, token, assignment_id):
    context = {
        'error': False
    }
    try:
        course_reg = validate_access(token, request, 'student')
        error, value = fetch_answer_to_this_assignment(
            request.user.student, assignment_id)
        print(error, value, assignment_id, "Na him be that")
        if not error:
            context['submitted_date'] = format_date(value.submission_date)
            context['answer'] = value.answer
        context['error'] = error
    except Exception as e:
        print(e, "Here ---<")
        context['error'] = True
    return JsonResponse(context, safe=True)


def student_view_post(request, token, stream_id):
    try:
        course_reg = validate_access(token, request, 'student')
        stream = Stream.objects.get(
            id=stream_id, course=course_reg.course, session=get_session())
        replies = StreamReply.objects.filter(stream=stream)
        form = AddReplyForm(request.POST or None)
        context = {
            'replies': replies,
            'course': course_reg,
            'post': stream,
            'form': form
        }
        if request.method == 'POST':
            if form.is_valid():
                this_form = form.save(commit=False)
                this_form.user = request.user
                this_form.stream = stream
                this_form.save()
                messages.success(request, "Comment added")
                return redirect(reverse('student_view_post', args=[token, stream.id]))
            else:
                messages.error(request, "Error")
        return render(request, path("classroom_view_post"), context)
    except Exception as e:
        print(e, "Here --- <")
        messages.error(request, "Access to this resource is denied")
        return redirect(reverse('student_view_post', args=[token, stream.id]))
