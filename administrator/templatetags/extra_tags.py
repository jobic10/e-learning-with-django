from django import template
from django.forms.fields import CheckboxInput
from e_learning.functions import get_session
from staff.models import CourseAllocation
from classroom.models import Submission, Assignment
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
