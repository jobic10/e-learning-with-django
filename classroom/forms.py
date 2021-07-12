from django import forms
from account.forms import FormSettings
from django.forms.widgets import DateInput, TextInput
from .models import *
from staff.models import CourseAllocation
from e_learning.functions import get_session


class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # super(AssignmentForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Assignment
        fields = ['question', 'expiry_date']
