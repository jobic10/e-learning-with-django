from account.forms import FormSettings
from student.models import *
from staff.models import Staff
from django import forms


class AddCourseForm(FormSettings):
    class Meta:
        model = Course
        fields = "__all__"


class AddDepartmentForm(FormSettings):
    class Meta:
        model = Department
        fields = "__all__"


class AddSessionForm(FormSettings):
    class Meta:
        model = Session
        fields = "__all__"


class AddStudentForm(FormSettings):
    class Meta:
        model = Student
        fields = "__all__"


class AddStaffForm(FormSettings):
    class Meta:
        model = Staff
        fields = "__all__"
