from django import template
from django.forms.fields import CheckboxInput
from e_learning.functions import get_session, format_date
from staff.models import CourseAllocation
from classroom.models import Submission, Assignment, StreamReply
register = template.Library()


@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)


@register.filter(name='lecturer')
def lecturer(value):
    lecturer = "No lecturer assigned yet"
    try:
        session = get_session()
        course = CourseAllocation.objects.get(
            course_id=int(value), session=session)
        lecturer = str(course.staff.admin)
    except:
        pass
    return lecturer


@register.filter(name='assignment_received')
def assignment_received(value):
    received = "None"
    assignment_id = int(value)
    try:
        session = get_session()
        assignment = Assignment.objects.get(id=assignment_id)
        received = Submission.objects.filter(assignment=assignment).count()
    except:
        pass
    return received


@register.simple_tag
def have_i_submitted(student, assignment_id):
    try:
        session = get_session()
        return Submission.objects.filter(student=student, assignment__id=assignment_id).exists()
    except:
        return False


@register.simple_tag
def when_did_i_submit(student, assignment_id):
    output = ""
    try:
        session = get_session()
        sub = Submission.objects.get(
            student=student, assignment__id=assignment_id)
        stamp = format_date(sub.submission_date)
        output = f"Turned in : {stamp}"
    except:
        output = ""
    return output


@register.filter(name='little')
def little(text):
    if len(text) > 80:
        return str(text[:80]) + "..."
    else:
        return text


@register.filter(name='comments')
def comments(the_id):
    count = StreamReply.objects.filter(id=the_id).count()
    if count == 1:
        text = "View the only comment"
    elif count > 1:
        text = f"View all {count} comments"
    else:
        text = "No comments yet, be the first"
    return text
