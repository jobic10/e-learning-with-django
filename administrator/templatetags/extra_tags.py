from django import template
from django.forms.fields import CheckboxInput
from e_learning.functions import get_session
from staff.models import CourseAllocation
register = template.Library()


@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)


@register.filter(name='lecturer')
def lecturer(value):
    print("Value is ", value)
    lecturer = "No lecturer assigned yet"
    try:
        session = get_session()
        course = CourseAllocation.objects.get(
            course_id=int(value), session=session)
        lecturer = str(course.staff.admin)
    except:
        pass
    return lecturer
