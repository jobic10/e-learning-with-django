from django.shortcuts import render
from .forms import *
# Administrative Functions


def path(html_file):
    return f"administrator/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)


def add_course(request):
    form = AddCourseForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, path('course'), context)
