from account.forms import FormSettings
from student.models import *


class AddCourseForm(FormSettings):
    class Meta:
        model = Course
        fields = "__all__"


class AddDepartmentForm(FormSettings):
    class Meta:
        model = Department
        fields = "__all__"
