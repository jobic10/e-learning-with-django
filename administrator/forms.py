from account.forms import FormSettings
from student.models import *
from staff.models import Staff
from django import forms
from .models import Settings


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
    department_list = Department.objects.filter(is_general=False)
    department = forms.ModelChoiceField(
        label="Choose Department", queryset=department_list, required=True)

    class Meta:
        model = Student
        exclude = ['admin']
        # https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }


class AddStaffForm(FormSettings):
    department_list = Department.objects.filter(is_general=False)
    department = forms.ModelChoiceField(
        label="Choose Department", queryset=department_list, required=True)

    class Meta:
        model = Staff
        exclude = ['admin']


class SettingsForm(FormSettings):
    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super(SettingsForm, self).clean()
        if not self.instance.pk and Settings.objects.exists():
            # if not self.pk and Settings.objects.exists():
            raise forms.ValidationError("Update Site Settings Instead")
            # ... do some cross-fields validation for the subclass
            # Finally, return the cleaned_data
        return cleaned_data

    class Meta:
        model = Settings
        fields = "__all__"
