from django import forms
from account.forms import FormSettings
from django.forms.widgets import DateInput, TextInput
from .models import *
from staff.models import CourseAllocation
from e_learning.functions import get_session
from django.core.exceptions import ValidationError


class AssignmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        # super(AssignmentForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Assignment
        fields = ['title', 'question', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Please select end date for submission'})
        }


class SubmissionForm(FormSettings):
    class Meta:
        model = Submission
        fields = ['answer']


class NewPostForm(FormSettings):
    class Meta:
        model = Stream
        fields = ['message']
        widgets = {
            'message': forms.Textarea()
        }
