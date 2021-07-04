from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from administrator.models import Course
from django.db.models import Q, OuterRef, Exists
from e_learning.functions import get_session

# Create your views here.


def path(html_file):
    return f"student/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)
