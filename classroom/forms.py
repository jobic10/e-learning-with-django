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

    # def clean_expiry_date(self):
    #     date = self.cleaned_data['expiry_date']
    #     import datetime
    #     if date <= datetime.datetime.today():
    #         raise ValidationError("Please select a future date")

    class Meta:
        model = Assignment
        fields = ['question', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Please select end date for submission'})
        }
